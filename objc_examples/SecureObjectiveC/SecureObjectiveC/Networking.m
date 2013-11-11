//
//  Networking.m
//  SecureObjectiveC
//
//  Created by nils on 16.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "Networking.h"

@implementation Networking
//- (void)allowAnyHTTPSCertificateForSomeHost {
//  NSHost *host = [NSHost hostWithName:@"google.de"];
//  [NSURLRequest setAllowsAnyHTTPSCertificate:YES forHost:host];
//}

- (void)cookies{
  NSHTTPCookieStorage *str = [NSHTTPCookieStorage sharedHTTPCookieStorage];
  // accept all cookies
  [str setCookieAcceptPolicy:NSHTTPCookieAcceptPolicyAlways];
  [str setCookieAcceptPolicy:NSHTTPCookieAcceptPolicyOnlyFromMainDocumentDomain];
}
@end
