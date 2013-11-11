//
//  CFuncArguments.m
//  SecureObjectiveC
//
//  Created by nils on 18.04.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

#import "CFuncArguments.h"

@implementation CFuncArguments

- (id)init{
  if (self = [super init]) {
    argTest(1, 2, 3, 4, 5, 6, 7);
    system("Date");
  }
  return self;
}

int argTest(int i1, int i2, int i3, int i4, int i5, int i6, int i7) {
  size_t numberOfBytes = 1024;
  uint8_t initializationVector[numberOfBytes];
  int tmp = i2;
  SecRandomCopyBytes(kSecRandomDefault,
                     (size_t) sizeof(initializationVector),
                     initializationVector);
  printf("%d%d%d%d%d%d%d", i1, i2, i3, i4, i5, i6, i7);
  return 1;
}
@end
