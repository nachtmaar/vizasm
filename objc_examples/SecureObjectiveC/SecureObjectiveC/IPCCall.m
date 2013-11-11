//
//  IPCCall.m
//  SecureObjectiveC
//
//  Created by nils on 07.10.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "IPCCall.h"

@implementation IPCCall

+ (void)ipcCall{
  [[UIApplication sharedApplication] openURL:[NSURL URLWithString:@"myApp://foo"]];
}
@end
