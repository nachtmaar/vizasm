//
//  LocationStuff.h
//  SecureObjectiveC
//
//  Created by nils on 16.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>

@interface LocationStuff : NSObject{
  CLLocationManager *locationManager;
}
@property (nonatomic, strong) CLLocationManager *locationManager;
@end
