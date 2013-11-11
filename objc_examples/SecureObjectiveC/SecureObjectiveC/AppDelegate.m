//
//  AppDelegate.m
//  SecureObjectiveC
//
//  Created by nils on 09.04.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "AppDelegate.h"
#import "SQLInjection.h"
#import "Streams.h"
#import "Entropy.h"
#import "FormatrString.h"
#import "SandboxStuff.h"

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
  [[SandboxStuff new] setSandboxProfiles];

//  //[[UntrustedSSLCertificate alloc] init];
//  [[Streams new] httpsConnection];
//  
//  SQLInjection *sql = [SQLInjection new];
//  //[sql sqlInjection];
//  
//  [[Entropy new] entropy];
//  [[FormatrString new] formatString];
  [Streams new];
}



@end
