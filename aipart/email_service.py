"""
Email service using SendGrid API (FREE - 100 emails/day)
Works on Render Free tier (no SMTP port blocking issues)
"""
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SendGrid Configuration
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@hera.work')  # Your verified sender email


def send_email_via_sendgrid(to_email, subject, html_content, attachment_path=None):
    """
    Send email using SendGrid API
    
    Args:
        to_email (str): Recipient email
        subject (str): Email subject
        html_content (str): HTML email body
        attachment_path (str): Optional path to file attachment
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Create message
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        # Attach file if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                encoded_file = base64.b64encode(file_data).decode()
                
                filename = os.path.basename(attachment_path)
                
                attached_file = Attachment(
                    FileContent(encoded_file),
                    FileName(filename),
                    FileType('application/pdf'),
                    Disposition('attachment')
                )
                message.attachment = attached_file
        
        # Send email via SendGrid API
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"✅ Email sent successfully to {to_email} (Status: {response.status_code})")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def send_payment_confirmation(to_email, order_details):
    """
    Send payment confirmation email immediately after successful payment
    
    Args:
        to_email (str): Customer email address
        order_details (dict): Order information (format, bookType, pages, theme, amount)
    
    Returns:
        bool: True if sent successfully
    """
    format_type = order_details.get('format', 'pdf')
    book_type = order_details.get('bookType', 'blackwhite')
    pages = order_details.get('pages', 24)
    theme = order_details.get('theme', 'Custom')
    amount = order_details.get('amount', '9.99')
    
    subject = "🎉 Payment Confirmed - Your Coloring Book is Being Created!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #E891C8 0%, #A97DC0 50%, #5EB3E4 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; margin-top: 20px; }}
            .order-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .timeline {{ margin: 30px 0; }}
            .timeline-item {{ display: flex; align-items: center; margin: 15px 0; }}
            .timeline-icon {{ font-size: 24px; margin-right: 15px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎨 Payment Confirmed!</h1>
                <p>Your custom coloring book is on its way</p>
            </div>
            
            <div class="content">
                <h2>Thank you for your order! 🎉</h2>
                <p>We've received your payment of <strong>${amount} USD</strong> and your coloring book is being created right now.</p>
                
                <div class="order-details">
                    <h3>📦 Order Details</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>📄 <strong>Format:</strong> {format_type.upper()}</li>
                        <li>🎨 <strong>Type:</strong> {book_type.replace('blackwhite', 'Black & White').title()}</li>
                        <li>📖 <strong>Pages:</strong> {pages}</li>
                        <li>🌟 <strong>Theme:</strong> {theme}</li>
                    </ul>
                </div>
                
                <div class="timeline">
                    <h3>⏰ What Happens Next?</h3>
                    <div class="timeline-item">
                        <span class="timeline-icon">✅</span>
                        <div>
                            <strong>Step 1: Payment Confirmed</strong><br>
                            <small style="color: #28a745;">Completed just now</small>
                        </div>
                    </div>
                    <div class="timeline-item">
                        <span class="timeline-icon">🎨</span>
                        <div>
                            <strong>Step 2: AI Generation</strong><br>
                            <small style="color: #007bff;">In progress... (10-30 minutes)</small>
                        </div>
                    </div>
                    <div class="timeline-item">
                        <span class="timeline-icon">📧</span>
                        <div>
                            <strong>Step 3: Email Delivery</strong><br>
                            <small style="color: #6c757d;">Arriving soon</small>
                        </div>
                    </div>
                </div>
                
                <p style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                    ⏳ <strong>Please wait 10-30 minutes</strong> while our AI creates {pages} unique coloring pages for you.
                    You'll receive another email with your complete book as a PDF attachment!
                </p>
            </div>
            
            <div class="footer">
                <p>Questions? Reply to this email or contact us at support@hera.work</p>
                <p>© 2025 Hera - Custom AI Coloring Books</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email_via_sendgrid(to_email, subject, html_content)


def send_pdf_email(to_email, pdf_path, book_details):
    """
    Send the generated PDF coloring book via email
    
    Args:
        to_email (str): Recipient email address
        pdf_path (str): Path to the generated PDF file
        book_details (dict): Dictionary containing book information
    
    Returns:
        bool: True if sent successfully
    """
    pages = book_details.get('pages', 24)
    book_type = book_details.get('bookType', 'blackwhite')
    theme = book_details.get('theme', 'Custom')
    
    subject = f"🎨 Your Custom Coloring Book is Ready!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #E891C8 0%, #A97DC0 50%, #5EB3E4 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; margin-top: 20px; }}
            .button {{ background: linear-gradient(135deg, #E891C8, #A97DC0); color: white; 
                      padding: 15px 30px; text-decoration: none; border-radius: 25px; 
                      display: inline-block; margin-top: 20px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Your Coloring Book is Ready!</h1>
            </div>
            
            <div class="content">
                <h2>Your masterpiece has arrived! 🎨</h2>
                <p>We're excited to share your custom coloring book with you. Your PDF is attached to this email!</p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>📚 Book Details</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>🎨 <strong>Type:</strong> {book_type.replace('blackwhite', 'Black & White').title()}</li>
                        <li>📖 <strong>Pages:</strong> {pages} pages</li>
                        <li>🌟 <strong>Theme:</strong> {theme}</li>
                    </ul>
                </div>
                
                <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; border-left: 4px solid #0c5460;">
                    <strong>📎 Your coloring book PDF is attached to this email!</strong><br>
                    <small>Simply open the attachment and start coloring! 🖍️</small>
                </div>
                
                <p style="margin-top: 30px;">
                    <strong>Tips for printing:</strong><br>
                    • Print on thick paper (cardstock recommended)<br>
                    • Use high quality settings for best results<br>
                    • Perfect for markers, crayons, and colored pencils!
                </p>
                
                <p style="margin-top: 30px;">
                    We hope you enjoy your custom coloring book! If you have any questions or want to create another book, 
                    visit our website anytime.
                </p>
            </div>
            
            <div class="footer">
                <p>Thank you for choosing Hera! ❤️</p>
                <p>Questions? Reply to this email or contact us at support@hera.work</p>
                <p>© 2025 Hera - Custom AI Coloring Books</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email_via_sendgrid(to_email, subject, html_content, pdf_path)


def send_physical_book_confirmation(to_email, order_details):
    """
    Send confirmation email for physical book orders
    
    Args:
        to_email (str): Customer email address
        order_details (dict): Order information including shipping address
    
    Returns:
        bool: True if sent successfully
    """
    pages = order_details.get('pages', 24)
    theme = order_details.get('theme', 'Custom')
    shipping = order_details.get('shipping', {})
    
    subject = "📦 Physical Book Order Confirmed - Shipping Soon!"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #E891C8 0%, #A97DC0 50%, #5EB3E4 100%); 
                       color: white; padding: 30px; text-align: center; border-radius: 10px; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; margin-top: 20px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📦 Physical Book Order Confirmed!</h1>
            </div>
            
            <div class="content">
                <h2>Your book is being printed! 🎨</h2>
                <p>We've received your order for a physical coloring book. It will be professionally printed and shipped to:</p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>📍 Shipping Address</h3>
                    <p>
                        {shipping.get('name', 'N/A')}<br>
                        {shipping.get('address', 'N/A')}<br>
                        {shipping.get('city', '')}, {shipping.get('postal_code', '')}<br>
                        {shipping.get('country', '')}
                    </p>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    ⏳ <strong>Estimated delivery:</strong> 5-10 business days<br>
                    You'll receive a tracking number once your book ships!
                </div>
                
                <p>Your book contains <strong>{pages} pages</strong> of <strong>{theme}</strong> themed coloring content.</p>
            </div>
            
            <div class="footer">
                <p>Questions? Reply to this email or contact us at support@hera.work</p>
                <p>© 2025 Hera - Custom AI Coloring Books</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email_via_sendgrid(to_email, subject, html_content)
