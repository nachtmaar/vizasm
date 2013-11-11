// Schocken

// Created by nils on 14.04.13.
//
//


#import <Foundation/Foundation.h>

@interface NSURLRequest (AnyHttpsCert)

+ (BOOL)allowsAnyHTTPSCertificateForHost:(NSString*)host;
@end