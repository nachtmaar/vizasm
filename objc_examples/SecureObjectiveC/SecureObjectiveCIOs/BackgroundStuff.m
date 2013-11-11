//
//  BackgroundStuff.m
//  SecureObjectiveC
//
//  Created by nils on 20.10.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "BackgroundStuff.h"

@implementation BackgroundStuff
@synthesize backgroundTask;

/** See: http://www.raywenderlich.com/29948/backgrounding-for-ios */ 
- (void)backgroundStuff{
  self.backgroundTask = [[UIApplication sharedApplication] beginBackgroundTaskWithExpirationHandler:^{
    NSLog(@"New background task");
  }];
  [[UIApplication sharedApplication] endBackgroundTask:self.backgroundTask];
}

@end
