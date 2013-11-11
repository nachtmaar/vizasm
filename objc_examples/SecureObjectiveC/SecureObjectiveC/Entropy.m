// Schocken

// Created by nils on 15.04.13.
//
//


#import "Entropy.h"
#import "FormatrString.h"
@implementation Entropy {

}

- (void)entropy{
	int rd1 = rand();
	int rd2 = random();
	int rd3 = arc4random();
	int randomResult = 0;
  size_t numberOfBytes = 1024;
  uint8_t initializationVector[numberOfBytes];
  SecRandomCopyBytes(kSecRandomDefault,
                     (size_t) sizeof(initializationVector),
                     initializationVector);
  [[[FormatrString alloc] init] formatString:@"%@%"];
}

@end