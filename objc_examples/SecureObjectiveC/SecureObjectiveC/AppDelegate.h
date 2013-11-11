//
//  AppDelegate.h
//  SecureObjectiveC
//
//  Created by nils on 09.04.13.
//  Copyright (c) 2013 nils. All rights reserved.
//

// The following source code has been written to see how it gets translated to assembler code.
// The source is not written very good nor does it have any semantic meaning.
// It think it doesn't even run. So do not complain!
// Just compile it and throw it into Hopper if you want
//
// This project tries to mention a few things on which the built-in filters of VizAsm will match

#import <Cocoa/Cocoa.h>
#import "UntrustedSSLCertificate.h"
#import "NSURLRequest+AnyHttpsCert.h"
#import "FormatrString.h"


@interface AppDelegate : NSObject <NSApplicationDelegate>

@property (assign) IBOutlet NSWindow *window;

@end
