Built-in filters
================

You can list the available build-in filters with "/VizAsm.py -lf <arch>" where arch is x86, x86_64 or arm.

.. code-block:: sh

	/.VizAsm.py -lf arm

	NSUserDefaultsFilter:
	Filters all NSUserDefault access

	UntrustedSSLCertsFilter:
	Check if invalid SSL certificates are being accepted

	RandomFuncFilter:
	Look out for functions generating random values: rand, random, arc4random

	FormatStringFilter:
	Check for exploitable log function (printf and NSLog)

	CFStreamSSLLevelFilter:
	Check the SSL level of a CFStream. Available levels are: kCFStreamSocketSecurityLevelNone, kCFStreamSocketSecurityLevelTLSv1,, kCFStreamSocketSecurityLevelSSLv2, kCFStreamSocketSecurityLevelSSLv3, kCFStreamSocketSecurityLevelNegotiatedSSL

	NSStreamSSLLevelFilter:
	Check the SSL level of a NSStream. Available levels are: NSStreamSocketSecurityLevelNone, NSStreamSocketSecurityLevelTLSv1, NSStreamSocketSecurityLevelSSLv2, NSStreamSocketSecurityLevelSSLv3, NSStreamSocketSecurityLevelNegotiatedSSL 

	IPCFilter:
	Check if the app has configured its own URL handler (iOS only) or does any interprocess communication call 

	SQLiteFilter:
	Filter exploitable sqlite3 calls (if the c function arguments heuristic is enabled!). Otherwise all sqlite3 calls will be filtered.

	CookiePolicyFilter:
	Check if a special cookie policy has been set. Available policies: NSHTTPCookieAcceptPolicyAlways, NSHTTPCookieAcceptPolicyNever, NSHTTPCookieAcceptPolicyOnlyFromMainDocumentDomain

	KeyChainFilter:
	Check for Keychain usage

	GeoLocationFilter:
	Check which geo information are retrieved and which accuracy level is set. Available levels: kCLLocationAccuracyBestForNavigation, kCLLocationAccuracyBest, kCLLocationAccuracyNearestTenMeters, kCLLocationAccuracyHundredMeters, kCLLocationAccuracyKilometer, kCLLocationAccuracyThreeKilometers

	SeatBeltFilter:
	Check if a special sandbox profile has been set. Available profiles are: kSBXProfileNoWriteExceptTemporary, kSBXProfileNoWrite, kSBXProfileNoNetwork, kSBXProfilePureComputation, kSBXProfileNoInternet

	DataProtectionFilter:
	Check for data storage via NSFileManager and NS(Mutable)Data (iOS only).
	Available options for NS(Mutable)Data writing are: NSDataWritingFileProtectionNone (0x10000000), NSDataWritingFileProtectionComplete (0x20000000), NSDataWritingFileProtectionMask (0xf0000000), NSDataWritingFileProtectionCompleteUnlessOpen (0x30000000), NSDataWritingFileProtectionCompleteUntilFirstUserAuthentication (0x40000000),
	Available options for NSFileManager writing are: NSFileProtectionNone, NSFileProtectionComplete, NSFileProtectionCompleteUnlessOpen, NSFileProtectionCompleteUntilFirstUserAuthentication


	UIPasteBoardFilter:
	Check for UIPasteboard usage 

	BackgroundTasksFilter:
	Check for background tasks