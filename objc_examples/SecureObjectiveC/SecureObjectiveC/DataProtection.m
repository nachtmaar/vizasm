//
//  DataProtection.m
//  SecureObjectiveC
//
//  Created by nils on 16.09.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "DataProtection.h"

@implementation DataProtection
// source: http://stackoverflow.com/questions/5155789/implementing-and-testing-ios-data-protection
- (void)dataProtectionStuff{
#ifdef TARGET_OS_IPHONE
  NSDictionary *dict = [NSDictionary dictionaryWithObject:NSFileProtectionComplete
                                                   forKey:NSFileProtectionKey];
  
  // create protected file
  [[NSFileManager defaultManager] createFileAtPath:@"some file path"
                                          contents:[@"super secret file contents" dataUsingEncoding:NSUTF8StringEncoding]
                                        attributes:dict];

  // TODO: also for mac ???
  // just an stupid example
  NSError *error;
  NSMutableData *data = [NSMutableData dataWithCapacity:1];
  [data writeToURL:[NSURL URLWithString:@"http://foo.com"] options:NSDataWritingFileProtectionComplete error:&error];
#endif
}
@end
