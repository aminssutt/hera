"""
Queue system to prevent memory overload on Render
Allows only 1 book generation at a time
"""
import threading
from queue import Queue
from datetime import datetime

# Global queue for book generation jobs
generation_queue = Queue()
is_processing = threading.Lock()
current_job = None

def add_to_queue(session_data):
    """Add a generation job to the queue"""
    job_id = session_data.get('id', datetime.now().strftime('%Y%m%d_%H%M%S'))
    
    print(f"\n📥 Adding job {job_id} to queue")
    print(f"   Queue size before: {generation_queue.qsize()}")
    
    generation_queue.put({
        'id': job_id,
        'session': session_data,
        'timestamp': datetime.now()
    })
    
    print(f"   Queue size after: {generation_queue.qsize()}")
    return job_id

def process_queue():
    """Process jobs one at a time from the queue"""
    global current_job
    
    while True:
        try:
            # Wait for a job (blocking)
            job = generation_queue.get()
            
            with is_processing:
                current_job = job
                
                print(f"\n{'='*60}")
                print(f"🔄 Processing job {job['id']}")
                print(f"   Queued at: {job['timestamp']}")
                print(f"   Jobs remaining in queue: {generation_queue.qsize()}")
                print(f"{'='*60}\n")
                
                # Import here to avoid circular imports
                from book_generator import generate_complete_book
                
                # Generate the book
                pdf_path = generate_complete_book(job['session'], preview_image_base64=None)
                
                if pdf_path:
                    print(f"✅ Job {job['id']} completed successfully")
                else:
                    print(f"❌ Job {job['id']} failed")
                
                current_job = None
                generation_queue.task_done()
                
        except Exception as e:
            print(f"❌ Error processing job: {str(e)}")
            import traceback
            traceback.print_exc()
            current_job = None
            generation_queue.task_done()

def start_queue_worker():
    """Start the queue processing worker thread"""
    worker = threading.Thread(target=process_queue, daemon=True)
    worker.start()
    print("✅ Queue worker started")

def get_queue_status():
    """Get current queue status"""
    return {
        'queue_size': generation_queue.qsize(),
        'is_processing': current_job is not None,
        'current_job': current_job['id'] if current_job else None
    }
