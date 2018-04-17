//
//  DataExtract.h
//  
//
//  Created by Rakhitha Chandrasekara on 10/2/15.
//
//

#ifndef ____DataExtract__
#define ____DataExtract__

#include <stdio.h>
void ReArrangeFrame(int* FrameBytes);
//void ReArrangeFrame(unsigned char* framebytes);
void ReConstructData(unsigned char* framebytes);
void ReconstructHealthData(unsigned char* framebytes);

#endif /* defined(____DataExtract__) */
