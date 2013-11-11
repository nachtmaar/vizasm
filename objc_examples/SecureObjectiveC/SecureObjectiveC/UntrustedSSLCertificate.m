//
//  UntrustedSSLCertificate.m
//  SecureObjectiveC
//
//  Created by nils on 09.04.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "UntrustedSSLCertificate.h"

int MyStreamSocketSecurityLevelKey = 2;

@implementation UntrustedSSLCertificate

//http://stackoverflow.com/questions/933331/how-to-use-nsurlconnection-to-connect-with-ssl-for-an-untrusted-cert/2033823#2033823

- (id)init{
  if((self = [super init])) {
    NSURLRequest* req = [NSURLRequest requestWithURL:[NSURL URLWithString:@"http://www.google.com"]];
    NSLog(@"%@", req);
    [self usePrivateApiToAllowHTTPSCert:[NSHost hostWithName:@"google.com"]];
  }
  return self;
}

/** Source: http://stackoverflow.com/questions/2001565/alternative-method-for-nsurlrequests-private-setallowsanyhttpscertificateforh */
- (void)usePrivateApiToAllowHTTPSCert:(NSHost *)host{
  SEL selx2 = @selector(setAllowsAnyHTTPSCertificate:forHost:);
  NSLog(@"%@", selx2);
  SEL selx = NSSelectorFromString(@"setAllowsAnyHTTPSCertificate:forHost:");
  if ( [NSURLRequest respondsToSelector: selx] ) {
    IMP fp;
    
    fp = [NSURLRequest methodForSelector:selx];
    
    (fp)([NSURLRequest class], selx, YES, host);
  }
}

- (BOOL)connection:(NSURLConnection *)connection canAuthenticateAgainstProtectionSpace:(NSURLProtectionSpace *)protectionSpace {
  return [protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodServerTrust];
}

- (void)connection:(NSURLConnection *)connection didReceiveAuthenticationChallenge:(NSURLAuthenticationChallenge *)challenge {
  [challenge.sender continueWithoutCredentialForAuthenticationChallenge:challenge];
}

@end
