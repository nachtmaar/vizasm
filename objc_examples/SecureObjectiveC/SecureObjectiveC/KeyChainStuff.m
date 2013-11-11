//
//  KeyChainStuff.m
//  SecureObjectiveC
//
//  Created by nils on 16.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "KeyChainStuff.h"
#import <Security/Security.h>

/** See:
 http://stackoverflow.com/questions/11535639/how-to-use-keychain-for-saving-password-like-generickeychain-sample-code
 http://stackoverflow.com/questions/7822892/pointer-casting-with-arc
 */

@implementation KeyChainStuff

- (void)keychainStuff{
  NSString *server = @"someServer";
  [self saveUsername:@"max" withPassword:@"secret" forServer:server];
  [self getCredentialsForServer:server];
  [self removeAllCredentialsForServer:server];
}

-(void) saveUsername:(NSString*)user withPassword:(NSString*)pass forServer:(NSString*)server {
  
  // Create dictionary of search parameters
  NSDictionary* dict = [NSDictionary dictionaryWithObjectsAndKeys:(__bridge id)(kSecClassInternetPassword),  kSecClass, server, kSecAttrServer, kCFBooleanTrue, kSecReturnAttributes, nil];
  
  // Remove any old values from the keychain
  OSStatus err = SecItemDelete((__bridge CFDictionaryRef) dict);
  
  // Create dictionary of parameters to add
  NSData* passwordData = [pass dataUsingEncoding:NSUTF8StringEncoding];
  dict = [NSDictionary dictionaryWithObjectsAndKeys:(__bridge id)(kSecClassInternetPassword), kSecClass, server, kSecAttrServer, passwordData, kSecValueData, user, kSecAttrAccount, nil];
  
  // Try to save to keychain
  err = SecItemAdd((__bridge CFDictionaryRef) dict, NULL);
  
}

-(void) removeAllCredentialsForServer:(NSString*)server {
  
  // Create dictionary of search parameters
  NSDictionary* dict = [NSDictionary dictionaryWithObjectsAndKeys:(__bridge id)(kSecClassInternetPassword),  kSecClass, server, kSecAttrServer, kCFBooleanTrue, kSecReturnAttributes, kCFBooleanTrue, kSecReturnData, nil];
  
  // Remove any old values from the keychain
  SecItemDelete((__bridge CFDictionaryRef) dict);
  
}

-(void) getCredentialsForServer:(NSString*)server {
  
  // Create dictionary of search parameters
  NSDictionary* dict = [NSDictionary dictionaryWithObjectsAndKeys:(__bridge id)(kSecClassInternetPassword),  kSecClass, server, kSecAttrServer, kCFBooleanTrue, kSecReturnAttributes, nil];
  
  
  CFDataRef foundRef;
  SecItemCopyMatching((__bridge CFDictionaryRef)dict, (CFTypeRef *)&foundRef);
}

@end
