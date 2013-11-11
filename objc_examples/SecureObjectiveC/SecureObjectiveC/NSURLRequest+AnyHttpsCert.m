// Schocken

// Created by nils on 14.04.13.
//
//


#import "NSURLRequest+AnyHttpsCert.h"

@implementation NSURLRequest (AnyHttpsCert)

// source: http://www.cocoanetics.com/2009/11/ignoring-certificate-errors-on-nsurlrequest/
//         http://stackoverflow.com/questions/933331/how-to-use-nsurlconnection-to-connect-with-ssl-for-an-untrusted-cert/
+ (BOOL)allowsAnyHTTPSCertificateForHost:(NSString *)host {
	return YES;
}



@end