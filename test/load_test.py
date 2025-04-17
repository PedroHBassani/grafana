import requests
import time
import random
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def make_request(url, session, request_id):
    """Make a single request to the API and log the result"""
    start_time = time.time()
    try:
        response = session.get(url)
        elapsed = time.time() - start_time
        status = response.status_code
        
        if status == 200:
            logger.info(f"Request {request_id}: Success ({status}) in {elapsed:.4f}s")
        else:
            logger.warning(f"Request {request_id}: Failed with status {status} in {elapsed:.4f}s")
            
        return True, elapsed, status
    except requests.RequestException as e:
        elapsed = time.time() - start_time
        logger.error(f"Request {request_id}: Error - {str(e)} in {elapsed:.4f}s")
        return False, elapsed, None

def run_load_test(url, total_requests=None, rate=10, concurrent=1, duration=None):
    """Run a load test against the specified API URL"""
    session = requests.Session()
    request_count = 0
    start_time = time.time()
    success_count = 0
    error_count = 0
    response_times = []
    
    logger.info(f"Starting load test against {url}")
    logger.info(f"Configuration: rate={rate}/s, concurrency={concurrent}, " +
                f"{'duration=' + str(duration) + 's' if duration else 'requests=' + str(total_requests)}")
    
    # Calculate delay between batches to achieve requested rate
    delay = concurrent / rate if rate > 0 else 0
    
    try:
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            while True:
                batch_start = time.time()
                
                # Submit a batch of concurrent requests
                futures = [executor.submit(make_request, url, session, request_count + i) 
                          for i in range(concurrent)]
                
                # Process the results
                for future in futures:
                    success, elapsed, _ = future.result()
                    request_count += 1
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                    response_times.append(elapsed)
                
                # Check if we've reached our target
                if total_requests and request_count >= total_requests:
                    break
                
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Sleep to maintain the requested rate
                elapsed_batch = time.time() - batch_start
                if delay > elapsed_batch:
                    time.sleep(delay - elapsed_batch)
                
                # Print stats every 50 requests
                if request_count % 50 == 0:
                    elapsed_total = time.time() - start_time
                    actual_rate = request_count / elapsed_total
                    logger.info(f"Progress: {request_count} requests, " +
                                f"Rate: {actual_rate:.2f} req/s, " +
                                f"Avg response: {sum(response_times)/len(response_times):.4f}s")
    
    except KeyboardInterrupt:
        logger.info("Load test interrupted by user")
    
    # Print final stats
    total_time = time.time() - start_time
    avg_response = sum(response_times) / len(response_times) if response_times else 0
    logger.info("\n" + "="*50)
    logger.info(f"Load Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*50)
    logger.info(f"Target URL:           {url}")
    logger.info(f"Total requests:       {request_count}")
    logger.info(f"Successful requests:  {success_count} ({success_count/request_count*100:.1f}%)")
    logger.info(f"Failed requests:      {error_count} ({error_count/request_count*100:.1f}%)")
    logger.info(f"Total time:           {total_time:.2f} seconds")
    logger.info(f"Average response time:{avg_response:.4f} seconds")
    logger.info(f"Actual request rate:  {request_count/total_time:.2f} requests/second")
    logger.info("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='API Load Testing Tool')
    parser.add_argument('--url', default='http://localhost:8000', help='Target API URL')
    parser.add_argument('--requests', type=int, help='Total number of requests to make')
    parser.add_argument('--duration', type=int, help='Test duration in seconds')
    parser.add_argument('--rate', type=float, default=10, help='Request rate per second')
    parser.add_argument('--concurrent', type=int, default=1, help='Number of concurrent requests')
    
    args = parser.parse_args()
    
    if not args.requests and not args.duration:
        parser.error("Either --requests or --duration must be specified")
    
    run_load_test(
        url=args.url,
        total_requests=args.requests,
        duration=args.duration,
        rate=args.rate,
        concurrent=args.concurrent
    )
