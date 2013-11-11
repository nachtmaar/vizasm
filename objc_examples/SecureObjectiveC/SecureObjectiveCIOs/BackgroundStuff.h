//
//  BackgroundStuff.h
//  SecureObjectiveC
//
//  Created by nils on 20.10.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface BackgroundStuff : NSObject{
  UIBackgroundTaskIdentifier backgroundTask;
}

@property (atomic) UIBackgroundTaskIdentifier backgroundTask;

- (void)backgroundStuff;

@end
