import os
import json
import stripe
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Promotion settings
PROMO_LIMIT = int(os.getenv('PROMO_FIRST_CUSTOMERS', 100))
PROMO_PRICE = float(os.getenv('PROMO_PRICE', 1.99))
REGULAR_PRICE = float(os.getenv('REGULAR_PRICE', 9.99))
COUNTER_FILE = 'order_counter.json'

def get_order_count():
    """Get current order count"""
    try:
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, 'r') as f:
                data = json.load(f)
                return data.get('total_orders', 0)
        return 0
    except:
        return 0

def increment_order_count():
    """Increment order count and return new count"""
    try:
        count = get_order_count()
        count += 1
        with open(COUNTER_FILE, 'w') as f:
            json.dump({
                'total_orders': count,
                'promo_orders': min(count, PROMO_LIMIT),
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
        return count
    except Exception as e:
        print(f"Error updating counter: {e}")
        return count

def get_current_price():
    """Get current price based on order count"""
    count = get_order_count()
    if count < PROMO_LIMIT:
        return PROMO_PRICE, True, PROMO_LIMIT - count  # price, is_promo, remaining_spots
    return REGULAR_PRICE, False, 0

# Create Blueprint
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/api/current-price', methods=['GET'])
def current_price():
    """Get current price and promo status"""
    price, is_promo, remaining = get_current_price()
    return jsonify({
        'price': price,
        'is_promo': is_promo,
        'remaining_spots': remaining,
        'promo_limit': PROMO_LIMIT,
        'regular_price': REGULAR_PRICE
    })

@payment_bp.route('/api/create-checkout', methods=['POST'])
def create_checkout():
    """Create a Stripe Checkout Session for book purchase"""
    try:
        data = request.json
        format_type = data.get('format', 'pdf')  # 'pdf' or 'physical'
        book_type = data.get('bookType', 'blackwhite')  # 'blackwhite' or 'colored'
        selections = data.get('selections', {})
        # No preview image - we'll regenerate all pages fresh
        
        # Get current price (promotional or regular)
        base_price, is_promo, remaining = get_current_price()
        
        # Calculate price (in cents) - only PDF gets promo, physical stays same
        if format_type == 'pdf':
            amount = int(base_price * 100)  # Convert to cents
            if is_promo:
                print(f"🎉 PROMO APPLIED: ${base_price} (Spot #{get_order_count() + 1}/{PROMO_LIMIT})")
        else:
            amount = 2499  # Physical book stays $24.99
        
        # Calculate page count
        pages = selections.get('pages', 24)
        if book_type == 'colored':
            bw_pages = pages // 2
            colored_pages = pages // 2
            description = f"{bw_pages} B&W + {colored_pages} Colored pages = {pages} total"
        else:
            description = f"{pages} Black & White coloring pages"
        
        # Add promo badge to description
        if format_type == 'pdf' and is_promo:
            description = f"🎉 LAUNCH PROMO #{get_order_count() + 1}/{PROMO_LIMIT} | {description}"
        
        # Prepare checkout session configuration
        session_config = {
            'payment_method_types': [
                'card',
                'kakao_pay',
                'naver_pay',
                'samsung_pay',
                'payco',
            ],
            'line_items': [{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Custom Kids Coloring Book',
                        'description': description,
                        'images': ['https://i.imgur.com/placeholder.png'],  # Optional: add a preview image
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            'mode': 'payment',
            'success_url': f"{os.getenv('FRONTEND_URL')}/success?session_id={{CHECKOUT_SESSION_ID}}",
            'cancel_url': f"{os.getenv('FRONTEND_URL')}/cancel",
            'customer_email': None,  # Let customer enter their email
            'metadata': {
                'format': format_type,
                'bookType': book_type,
                'pages': str(pages),
                'theme': ','.join(selections.get('theme', [])),
                'topic': selections.get('topic', ''),
                'difficulty': selections.get('difficulty', 'Easy'),
                'colors': json.dumps(selections.get('colors', [])),
                # No preview image - we'll regenerate all pages fresh
            }
        }
        
        # Add shipping address collection for physical books
        if format_type == 'physical':
            session_config['shipping_address_collection'] = {
                'allowed_countries': ['KR', 'US', 'CA', 'GB', 'FR', 'DE', 'JP', 'AU'],
            }
        
        # Create the checkout session
        session = stripe.checkout.Session.create(**session_config)
        
        return jsonify({
            'success': True,
            'checkout_url': session.url,
            'session_id': session.id
        })
        
    except Exception as e:
        print(f"Error creating checkout session: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@payment_bp.route('/api/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        # Verify webhook signature (if webhook secret is configured)
        if webhook_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        else:
            # For development without webhook secret
            event = json.loads(payload)
        
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            # Increment order counter for successful payment
            order_number = increment_order_count()
            
            print(f"\n{'='*60}")
            print(f"💳 Payment successful! Session ID: {session['id']}")
            print(f"🎯 Order #{order_number}")
            print(f"{'='*60}")
            
            # Extract customer info
            customer_email = session.get('customer_details', {}).get('email')
            amount = session.get('amount_total', 0) / 100  # Convert from cents
            
            # Extract metadata
            metadata = session.get('metadata', {})
            format_type = metadata.get('format', 'pdf')
            book_type = metadata.get('bookType', 'blackwhite')
            pages = int(metadata.get('pages', 24))
            theme = metadata.get('theme', 'Custom')
            
            print(f"📧 Customer: {customer_email}")
            print(f"💰 Amount: ${amount:.2f} USD")
            print(f"📦 Format: {format_type} | Type: {book_type} | Pages: {pages}")
            print(f"🎨 Theme: {theme}")
            
            # Show promo status
            if format_type == 'pdf' and order_number <= PROMO_LIMIT:
                print(f"🎉 PROMO ORDER: {order_number}/{PROMO_LIMIT}")
            print()
            
            # STEP 1: Send immediate payment confirmation email
            print("📨 Step 1: Sending payment confirmation email...")
            from email_service import send_payment_confirmation
            
            order_details = {
                'format': format_type,
                'bookType': book_type,
                'pages': pages,
                'theme': theme,
                'amount': f"{amount:.2f}",
                'order_number': order_number
            }
            
            confirmation_sent = send_payment_confirmation(customer_email, order_details)
            
            if confirmation_sent:
                print("✅ Payment confirmation sent!\n")
            else:
                print("⚠️ Payment confirmation failed, but continuing...\n")
            
            # STEP 2: Add to generation queue (prevents memory overload)
            print("📚 Step 2: Adding to generation queue...")
            
            from generation_queue import add_to_queue, get_queue_status
            
            # Add job to queue
            job_id = add_to_queue(session)
            queue_status = get_queue_status()
            
            print(f"✅ Job {job_id} added to queue!")
            print(f"   Queue position: {queue_status['queue_size']}")
            print(f"   Currently processing: {queue_status['current_job'] or 'None'}\n")
            print(f"{'='*60}\n")
            
        # Return success immediately (don't wait for generation)
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"❌ Webhook error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 400


@payment_bp.route('/api/session-status/<session_id>', methods=['GET'])
def get_session_status(session_id):
    """Get the status of a checkout session"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        return jsonify({
            'success': True,
            'status': session.payment_status,
            'customer_email': session.customer_details.email if session.customer_details else None,
            'amount_total': session.amount_total,
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@payment_bp.route('/api/generation-status/<session_id>', methods=['GET'])
def get_generation_status(session_id):
    """Get the generation status and PDF path for a session"""
    try:
        from session_manager import get_session_pdf
        from generation_queue import get_queue_status
        
        # Check if session has a completed PDF
        session_data = get_session_pdf(session_id)
        
        if session_data and session_data.get('status') == 'completed':
            return jsonify({
                'success': True,
                'status': 'completed',
                'pdf_filename': session_data['pdf_filename'],
                'message': 'Your book is ready! 🎉'
            })
        
        # Otherwise check queue status
        queue_status = get_queue_status()
        
        if queue_status['is_processing']:
            return jsonify({
                'success': True,
                'status': 'generating',
                'message': 'Your book is being generated... 🎨'
            })
        else:
            return jsonify({
                'success': True,
                'status': 'queued',
                'queue_position': queue_status['queue_size'],
                'message': f"Your book is in the queue (position: {queue_status['queue_size']})... 📚"
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@payment_bp.route('/api/download-pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    """Download a generated PDF"""
    try:
        import os
        from flask import send_file
        
        pdf_folder = os.path.join(os.path.dirname(__file__), 'generated_pdfs')
        pdf_path = os.path.join(pdf_folder, filename)
        
        if os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                mimetype='application/pdf',
                as_attachment=False,  # Display in browser
                download_name=filename
            )
        else:
            return jsonify({
                'success': False,
                'error': 'PDF not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@payment_bp.route('/api/contact-feedback', methods=['POST'])
def contact_feedback():
    """Handle contact form feedback submissions"""
    try:
        from email_service import send_email_via_sendgrid
        
        data = request.json
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')
        rating = data.get('rating', '')
        ease_of_use = data.get('easeOfUse', '')
        quality = data.get('quality', '')
        would_recommend = data.get('wouldRecommend', '')
        additional_comments = data.get('additionalComments', '')
        
        # Build feedback email body
        email_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #9333ea;">🎨 New Feedback from Hera User</h2>
            
            <div style="background: #f9fafb; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #6b7280;">👤 Contact Information</h3>
                <p><strong>Name:</strong> {first_name} {last_name}</p>
                <p><strong>Email:</strong> {email}</p>
            </div>
            
            <div style="background: #fef3c7; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #92400e;">⭐ Overall Rating: {rating}/5</h3>
            </div>
            
            <div style="background: #f9fafb; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #6b7280;">📊 Survey Responses</h3>
                <p><strong>Ease of Use:</strong> {ease_of_use}</p>
                <p><strong>Quality Rating:</strong> {quality}</p>
                <p><strong>Would Recommend:</strong> {would_recommend}</p>
            </div>
            
            {f'''
            <div style="background: #ede9fe; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #6b21a8;">💬 Additional Comments</h3>
                <p style="white-space: pre-wrap;">{additional_comments}</p>
            </div>
            ''' if additional_comments else ''}
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 12px;">
                <p>Received on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        """
        
        # Send feedback email to Hera
        send_email_via_sendgrid(
            to_email='contact@herastudio.art',
            subject=f'📢 New Feedback from {first_name} {last_name} - Rating: {rating}/5',
            html_content=email_body
        )
        
        # Send confirmation email to user
        confirmation_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #9333ea;">Thank You for Your Feedback! 💜</h2>
            
            <p>Hi {first_name},</p>
            
            <p>Thank you so much for taking the time to share your feedback with us! Your input is incredibly valuable and helps us make Hera better for everyone.</p>
            
            <div style="background: #f3e8ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p style="margin: 0;">We've received your feedback and our team will review it carefully. If you've reported an issue or have a question, we'll get back to you as soon as possible.</p>
            </div>
            
            <p>Keep creating amazing coloring books! 🎨</p>
            
            <p>Best regards,<br><strong>The Hera Team</strong></p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 12px;">
                <p>Questions? Contact us at: contact@herastudio.art</p>
            </div>
        </div>
        """
        
        send_email_via_sendgrid(
            to_email=email,
            subject='Thank you for your feedback! - Hera',
            html_content=confirmation_body
        )
        
        return jsonify({
            'success': True,
            'message': 'Feedback sent successfully'
        }), 200
        
    except Exception as e:
        print(f"Error sending feedback: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


