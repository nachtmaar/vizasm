//
//  LocationStuff.m
//  SecureObjectiveC
//
//  Created by nils on 16.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "LocationStuff.h"


// Source: http://stackoverflow.com/questions/17465929/how-to-track-user-location-in-background

@implementation LocationStuff
@synthesize locationManager;

- (id)init{
  if (self = [super init]) {
    self.locationManager = [[CLLocationManager alloc] init];
    self.locationManager.distanceFilter = kCLDistanceFilterNone;
    self.locationManager.desiredAccuracy = kCLLocationAccuracyBest;
    self.locationManager.delegate = self;
  }
  return self;
}


#pragma mark - CLLocationManager Delegate

- (void)locationManager:(CLLocationManager *)manager didUpdateToLocation:(CLLocation *)newLocation fromLocation:(CLLocation *)oldLocation {
  NSLog(@"updated from %@ to %@", oldLocation, newLocation);
}

@end
