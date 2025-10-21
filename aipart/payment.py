import os
import json
import stripe
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Create Blueprint
payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/api/create-checkout', methods=['POST'])
def create_checkout():
    """Create a Stripe Checkout Session for book purchase"""
    try:
        data = request.json
        format_type = data.get('format', 'pdf')  # 'pdf' or 'physical'
        book_type = data.get('bookType', 'blackwhite')  # 'blackwhite' or 'colored'
        selections = data.get('selections', {})
        # No preview image - we'll regenerate all pages fresh
        
        # Calculate price (in cents)
        amount = 999 if format_type == 'pdf' else 2499  # $9.99 or $24.99
        
        # Calculate page count
        pages = selections.get('pages', 24)
        if book_type == 'colored':
            bw_pages = pages // 2
            colored_pages = pages // 2
            description = f"{bw_pages} B&W + {colored_pages} Colored pages = {pages} total"
        else:
            description = f"{pages} Black & White coloring pages"
        
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
            
            print(f"\n{'='*60}")
            print(f"💳 Payment successful! Session ID: {session['id']}")
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
            print(f"🎨 Theme: {theme}\n")
            
            # STEP 1: Send immediate payment confirmation email
            print("📨 Step 1: Sending payment confirmation email...")
            from email_service import send_payment_confirmation
            
            order_details = {
                'format': format_type,
                'bookType': book_type,
                'pages': pages,
                'theme': theme,
                'amount': f"{amount:.2f}"
            }
            
            confirmation_sent = send_payment_confirmation(customer_email, order_details)
            
            if confirmation_sent:
                print("✅ Payment confirmation sent!\n")
            else:
                print("⚠️ Payment confirmation failed, but continuing...\n")
            
            # STEP 2: Generate the book in BACKGROUND using threading
            print("📚 Step 2: Queuing book generation in background...")
            
            import threading
            from book_generator import generate_complete_book
            
            # Launch generation in a separate thread to avoid blocking webhook
            def generate_in_background():
                try:
                    print(f"🔄 [Background] Starting book generation for {customer_email}...")
                    pdf_path = generate_complete_book(session, preview_image_base64=None)
                    
                    if pdf_path:
                        print(f"✅ [Background] Book generation complete! PDF saved at: {pdf_path}")
                    else:
                        print(f"❌ [Background] Book generation failed for {customer_email}")
                except Exception as e:
                    print(f"❌ [Background] Error in book generation: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            # Start background thread
            thread = threading.Thread(target=generate_in_background)
            thread.daemon = True
            thread.start()
            
            print(f"✅ Background generation started! Webhook responding immediately.\n")
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
