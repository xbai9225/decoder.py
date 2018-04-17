//
//  DataExtract.c
//  
//
//  Created by Rakhitha Chandrasekara on 10/01/2018.
//  This can fragment a 245 byte frame into 1s data chunks which contains 35 bytes
//  It discards the header byte and the crc checksum bytes
//  Another output is created for byte reconstructed data


#include "DataExtract.h"
#define FRAMESIZE 248
#define PACKETSIZE 35

FILE* fid;
FILE* fid1;
FILE* fid2;
FILE* fid3;
FILE* fid4;


unsigned char c=255;    // %d will print the decimal value
short int d = 32767;    // signed short int (2 bytes)
int b=2147483646;       // 4byte integer type, signed
int j=0;
int a;
int count=0;
int FrameBytes[PACKETSIZE];             // This is used to deframe the data from the OBC txt file
unsigned char framebytes[PACKETSIZE];   // This is used to reconstruct data using bytes
unsigned char NumberFrames=1;
unsigned char framecounter=0;

int main(){
    
    fid = fopen("0X10_Gallassia.txt","w");
    fid1 = fopen("EXP0000.txt","r");        // data from the OBC
    fid2 = fopen("0x10_Gallassia_reconstruct.txt","w");
    fid3 = fopen("0x10_Gallassia_final.txt","w");
    fid4 = fopen("0x10_Gallassia_healthStatus.txt","w");
    
    while (fscanf(fid1,"%d",&a) == 1) {
        
        count++;
        
        
        if ((count == 1) || (count == FRAMESIZE-1) || (count == FRAMESIZE)) {  // one frame
        
            if (count == FRAMESIZE) {
                count = 0;
                NumberFrames++;
                //printf("\n");   // end of frame
            }
            
            
            continue;           // discard the header byte and CRC bytes
        }
        
        
        FrameBytes[j]= a;
        framebytes[j]= a;
        j++;
        
        if(j == PACKETSIZE){ // FrameBytes from 0 to 7
            
            j=0;
            
            
            // printf("\n");
            ReArrangeFrame(FrameBytes);     // put a record (a frame) in byte format in rows
            //ReArrangeFrame(framebytes);
            ReConstructData(framebytes);
            
            
            // there are 21 lines (34 bytes each) in health status data
            if (framecounter < 21) {
                ReconstructHealthData(framebytes);
                framecounter++;
            }
            
            
            //if (NumberFrames < 4) {
                
            //    ReconstructHealthData(framebytes);
                
            //}
            
            
        }
        
        
        
    }// while
    
    printf("%d %d %d\n",b,c,d);
    
    fclose(fid);
    fclose(fid1);
    fclose(fid2);
    fclose(fid3);
    fclose(fid4);
    
    
    
    
    return 0;
}

//void ReArrangeFrame(unsigned char* framebytes){    // This also works only less resources in memory

void ReArrangeFrame(int* FrameBytes){

    
    int FrameSum = 0 ;
    int k=0;
    
    //for (k=0; k<PACKETSIZE; k++) {
    //    printf("%d ",FrameBytes[k]);
    //}
    //printf("\n");
    
    for (k=0; k<PACKETSIZE; k++) {
        fprintf(fid,"%d ",FrameBytes[k]);
    }
    
    fprintf(fid,"\n");
    
    
    
}

void ReConstructData(unsigned char* framebytes){
    
    unsigned char i,j,k;           // 1 byte
    unsigned short int temp;       // 2 bytes
    unsigned short int Reconsdata[PACKETSIZE/2];
    unsigned int temp32LSB,temp32MSB,temp32Intermediate;
    unsigned int APDcounts[7];    // APD1&2 top, bot , Coincidences and DAC values
    unsigned char Thermistors[5]; // 5x thermistor values
    unsigned short int LaserDAC;  // 2 bytes for laser dac
    unsigned short int LCPR_Parameters[4];    //
    unsigned int PDvoltT1T2;      // 4 bytes
    unsigned int temp1;
    unsigned int PDvoltage;
    //unsigned int Temperature1,Temperature2;
    unsigned int Humidity,Dummy,Temp;
    unsigned short int HumidityDecode;
    unsigned char HeatL_FLG,BMarkStable,LaserToken,Laser_Reinstated;
    unsigned short int LCD1DigitalValue_old;  // 11 bits needed
    unsigned short int LCD2DigitalValue_old;
    unsigned short int LaserDACDecode;
    
    
    // concantanates bytes in to 2byte format
    for (i=0,j=0 ; i < PACKETSIZE ; i = i + 2, j++) {
        
        temp = framebytes[i] & 0x00FF;
        temp = temp << 8;
        Reconsdata[j] = framebytes[i+1] + temp;
    }
    
    // put 2-byte data into fid2 file
    for (k=0; k< PACKETSIZE/2 ; k++) {
        fprintf(fid2,"%d ",Reconsdata[k]);
    }
    
    fprintf(fid2,"\n");
    
    temp32LSB = Reconsdata[0];
    temp32MSB = Reconsdata[1];
    temp32MSB = temp32MSB << 16;
    APDcounts[0] = (temp32MSB + temp32LSB) & 0x000FFFFF; // APD1 top counts,20 bits
    
    temp32Intermediate = (temp32MSB + temp32LSB) & 0xFFF00000;
    temp32Intermediate = temp32Intermediate >> 20;
    
    temp32MSB = Reconsdata[2];
    temp32MSB = temp32MSB & 0x000000FF;
    temp32MSB = temp32MSB << 12;
    APDcounts[1] = (temp32MSB + temp32Intermediate) & 0x000FFFFF; // APD2 top counts,20 bits
    
    temp32LSB = Reconsdata[2];
    temp32LSB = temp32LSB >> 8;
    temp32MSB = Reconsdata[3];
    temp32MSB = temp32MSB << 8;
    APDcounts[2] = (temp32MSB + temp32LSB) & 0x000FFFFF; // APD1 bottom counts,20 bits
    
    temp32LSB = Reconsdata[3];
    temp32LSB = temp32LSB >> 12;
    temp32MSB = Reconsdata[4];
    temp32MSB = temp32MSB << 12;
    
    APDcounts[3] = (temp32MSB + temp32LSB) & 0x000FFFFF; // APD2 bottom counts,20bits
    
    APDcounts[4] = Reconsdata[5] & 0x0000FFFF;  // Coincidences,16bits
    
    temp32LSB = Reconsdata[6];
    APDcounts[5] = temp32LSB & 0x00000FFF ; // APD1 dac,12bits
    
    temp32LSB = Reconsdata[6];
    temp32LSB = temp32LSB & 0x0000F000;
    temp32LSB = temp32LSB >> 12;
    
    temp32MSB = Reconsdata[7];
    temp32MSB = (temp32MSB << 4) & 0x00000FF0;
    
    APDcounts[6] = (temp32MSB + temp32LSB) & 0x00000FFF; // APD2 dac,12bits
    
    for(i = 0, j = 0; i < 4,j < 2; i = i+2, j++){
        Thermistors[i] = Reconsdata[8+j];
        temp = Reconsdata[8+j] >> 8;
        Thermistors[i+1] = temp & 0x00FF;
    }
    
    temp = Reconsdata[10];
    Thermistors[4] = temp & 0x00FF;     // 5x thermistors
    
    temp32LSB = Reconsdata[10];
    temp32LSB = temp32LSB >> 8;
    temp32MSB = Reconsdata[11];
    temp32MSB = temp32MSB << 8;
    LaserDAC = (temp32MSB + temp32LSB) & 0x0FFF; // laser DAC, 12bits
    
    // LCPR data decode
    temp32LSB = Reconsdata[11];
    temp32LSB = (temp32LSB >> 8) & 0x00FF;
    
    temp32MSB = Reconsdata[12];
    temp32MSB = temp32MSB << 4;
    
    LCPR_Parameters[0] = (temp32MSB + temp32LSB) & 0x0FFF;
    
    temp32LSB = Reconsdata[12];
    LCPR_Parameters[1] = (temp32LSB >> 4) & 0x0FFF; // LC_meas_capacitance_pF
    
    temp32LSB = Reconsdata[13];
    LCPR_Parameters[2] = temp32LSB & 0x0FFF; //uk_LCPR_1
    
    temp32LSB = Reconsdata[13];
    temp32LSB = temp32LSB >> 12;
    temp32MSB = Reconsdata[14];
    temp32MSB = temp32MSB << 4;
    LCPR_Parameters[3] = (temp32MSB+temp32LSB) & 0x0FFF; //uk_LCPR_2
    
    temp32LSB = Reconsdata[14];
    temp32LSB = (temp32LSB >> 8) & 0x00FF;
    
    temp32MSB = Reconsdata[15];
    temp32MSB = temp32MSB << 
    
    
    temp32LSB = Reconsdata[13];
    temp32MSB = Reconsdata[12];
    temp32MSB = temp32MSB << 16;
    PDvoltT1T2 = temp32MSB + temp32LSB;
    temp1 = PDvoltT1T2 & 0xFFC00000;
    PDvoltage = temp1 >> 22;                // photo diode voltage
    temp1 = PDvoltT1T2 & 0x003FF800;
    //Temperature1 = temp1 >> 11;             // Temperature near laser
    //Temperature2 = PDvoltT1T2 & 0x000007FF; // Temperature near APD
    
    Humidity = Reconsdata[14];              // Humidity
    Dummy = Reconsdata[15];
    Temp = Reconsdata[16];
    
    // 24/02/15
    HumidityDecode = Humidity;
    HeatL_FLG = (HumidityDecode & 0x4000)>>15; // 15th bit
    BMarkStable = (HumidityDecode & 0x2000)>>14; // 14th bit
    LaserToken = (HumidityDecode & 0x1000)>>13; // 13th bit
    Laser_Reinstated = (HumidityDecode & 0x0800)>>12; // 12th bit
    LCD1DigitalValue_old = (HumidityDecode & 0x07FF)*21-18; // 11 lsb, 8
    
    LaserDACDecode = Reconsdata[11];
    LCD2DigitalValue_old = ((LaserDACDecode & 0xFC00)>>10)*10;  // x *10+160 previous case
    
    
    
    for (k=0; k < 7 ; k++) {
        fprintf(fid3,"%d ",APDcounts[k]);
    }
    
    fprintf(fid3,"%d ",HeatL_FLG);
    fprintf(fid3,"%d ",BMarkStable);
    fprintf(fid3,"%d ",LaserToken);
    fprintf(fid3,"%d ",Laser_Reinstated);
    fprintf(fid3,"%d ",LaserDAC);
    fprintf(fid3,"%d ",PDvoltage);
    fprintf(fid3,"%d ",Temperature1);
    fprintf(fid3,"%d ",Temperature2);
    //fprintf(fid3,"%d ",Humidity);  //24/02/15 commented
    fprintf(fid3,"%d ",LCD1DigitalValue_old);
    fprintf(fid3,"%d ",LCD2DigitalValue_old);
    fprintf(fid3,"%d ",Dummy);
    fprintf(fid3,"%d ",Temp);
    fprintf(fid3,"\n");
    
    
}


void ReconstructHealthData(unsigned char* framebytes){

    unsigned char k;
    
    for (k=0; k<PACKETSIZE; k++) {
        fprintf(fid4,"%d ",framebytes[k]);
    }
    
    fprintf(fid4,"\n");
    
    
}















