// Schocken

// Created by nils on 15.04.13.
//
//


#import "Streams.h"

#import <CoreFoundation/CoreFoundation.h>
#import <CFNetwork/CFNetwork.h>
#import <CFNetwork/CFHTTPStream.h>
@implementation Streams {
  
}

- (id)init{
  if (self = [super init]) {
    [self nsStream];
    [self httpsConnection];
    cfstreamExample();
    
  }
  return self;
}
// source: http://www.cocoanetics.com/2009/11/ignoring-certificate-errors-on-nsurlrequest/
- (void)httpsConnection{
  
	NSString *url = @"https://192.168.1.3:443/";  // server name does not match
	NSURL *URL = [NSURL URLWithString:url];
	//[NSURLRequest setAllowsAnyHTTPSCertificate:YES forHost:[URL host]];
  
	NSURLRequest *request = [NSURLRequest requestWithURL:URL];
	NSURLResponse *response;
	NSError *error = nil;
	NSData *data = [NSURLConnection sendSynchronousRequest:request returningResponse:&response error:&error];
  
  
	if (error)
	{
		NSLog(@"error");
		NSLog(@"%@", [error localizedDescription]);
	}
	else
	{
		NSLog(@"no error");
		NSString *result = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
		NSLog(@"%@", result);
	}
}


/** Source: https://developer.apple.com/library/mac/documentation/Networking/Conceptual/CFNetwork/CFStreamTasks/CFStreamTasks.html#//apple_ref/doc/uid/TP30001132-CH6-SW1
 */
void cfstreamExample(void){
  CFURLRef fileURL = (__bridge CFURLRef)[NSURL fileURLWithPath:@"http://google.de"];
  // create stream
  CFReadStreamRef myReadStream = CFReadStreamCreateWithFile(kCFAllocatorDefault, fileURL);
  
  // open stream
  if (!CFReadStreamOpen(myReadStream)) {
    CFStreamError myErr = CFReadStreamGetError(myReadStream);
    // An error has occurred.
    if (myErr.domain == kCFStreamErrorDomainPOSIX) {
      // Interpret myErr.error as a UNIX errno.
    } else if (myErr.domain == kCFStreamErrorDomainMacOSStatus) {
      // Interpret myErr.error as a MacOS error code.
      OSStatus macError = (OSStatus)myErr.error;
      // Check other error domains.
    }
  }
  
  //Disable SSL
  CFReadStreamSetProperty(myReadStream, kCFStreamSSLLevel, kCFStreamSocketSecurityLevelNone);
  
  // read from stream
  CFIndex numBytesRead;
  do {
    UInt8 buf[1000]; // define myReadBufferSize as desired
    numBytesRead = CFReadStreamRead(myReadStream, buf, sizeof(buf));
  } while( numBytesRead > 0 );
  
  CFReadStreamClose(myReadStream);
  CFRelease(myReadStream);
  myReadStream = NULL;
}

// TODO: add source
- (void)nsStream{
#ifndef TARGET_OS_IPHONE
  // First we define the host to be contacted
  NSHost *myhost = [NSHost hostWithName:@"www.conglomco.com"]; // Then we create
  NSInputStream *myInputStream = nil;
  NSOutputStream *myOutputStream = nil;
  [NSStream getStreamsToHost:myhost
                        port:443 inputStream:&myInputStream
                outputStream:&myOutputStream];
  [myOutputStream setProperty:NSStreamSocketSecurityLevelNone // Note
                       forKey:NSStreamSocketSecurityLevelKey];
  //[myInputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
  [myInputStream open];
  myInputStream.delegate = self;
  NSLog(@"%@", [myInputStream description]);
#endif
}

- (void)stream:(NSInputStream *)iStream handleEvent:(NSStreamEvent)event {
  BOOL shouldClose = NO;
  switch(event) {
    case  NSStreamEventEndEncountered:
      shouldClose = YES;
      // If all data hasn't been read, fall through to the "has bytes" event
      if(![iStream hasBytesAvailable]) break;
    case NSStreamEventHasBytesAvailable: ; // We need a semicolon here before we can declare local variables
      
      break;
    case NSStreamEventErrorOccurred:
      // some other error
      shouldClose = YES;
      break;
  }
  if(shouldClose) [iStream close];
}

@end