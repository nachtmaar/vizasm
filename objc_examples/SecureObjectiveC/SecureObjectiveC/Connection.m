//
//  Connection.m
//  CocoaObjectcall
//
//  Created by nils on 09.04.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "Connection.h"

@implementation Connection

//http://stackoverflow.com/questions/933331/how-to-use-nsurlconnection-to-connect-with-ssl-for-an-untrusted-cert/2033823#2033823

- (id)init{
    if((self = [super init])) {
        
    }
    return self;
}
- (BOOL)connection:(NSURLConnection *)connection canAuthenticateAgainstProtectionSpace:(NSURLProtectionSpace *)protectionSpace {
    return [protectionSpace.authenticationMethod isEqualToString:NSURLAuthenticationMethodServerTrust];
}
- (void)connection:(NSURLConnection *)connection didReceiveAuthenticationChallenge:(NSURLAuthenticationChallenge *)challenge {
    [challenge.sender continueWithoutCredentialForAuthenticationChallenge:challenge];
}

@end
