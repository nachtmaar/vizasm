//
//  SandboxStuff.m
//  SecureObjectiveC
//
//  Created by nils on 08.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "SandboxStuff.h"
#import "sandbox.h"

@implementation SandboxStuff

- (id)init{
  if (self = [super init]) {
    [self setSandboxProfiles];
    
  }
  return self;
}

// TODO: CHECK sandbox for iOs > 6
/* Source: http://iphonedevwiki.net/index.php/Seatbelt */
- (void)setSandboxProfiles{
  char* errbuf;
  sandbox_init(kSBXProfileNoWrite, SANDBOX_NAMED, &errbuf);
}

@end
