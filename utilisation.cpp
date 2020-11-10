#include "rats.h"
#include <iostream>
#include <exception>
#include <sstream>
#include <string>
#include <fstream>
#include <vector>
#include <cmath>
#include <string.h>
#include <bits/stdc++.h>

using namespace std;

unsigned long long int factorial(long long int n);

unsigned long long int factorial(long long int n){
      if(n > 1)
          return n * factorial(n - 1);
      else
          return 1;
}

string simulator(int i){
  vector<long double> PsR1;
  vector<long double> PsR2;
  vector<long double> PsR3;

  cout<< "" <<endl;
  cout<<" Voice Simulator Running  ... "<<endl;

  long double prbbuV = 0.50;
  long double prbbuD = 1.00;
  long double revenueR1 =0, revenueR2 =0, revenueR3 = 0.0;

    // **** Create RAT Networks and the different service class ****
    RATattributes RAT1 (1, 10, 5);  //RATattributes( rid, capacity, threshold):
    RATattributes RAT2(2, 20, 10);
    RATattributes RAT3 (3, 30, 15);

    Services voice(1, 1);  //Services( sid, bbu):
    Services data(2, 2);

     RATloads ratesR1(1, i, 1);  // RATloads(rid, arv, dep) *In __calls/min*
     RATloads ratesR2(2, i, 1);
     RATloads ratesR3(3, i, 1);

    long double RAT1load = ratesR1.RATload(); // calculate loading for each RAT of class-i and returns [self.rid,PnewVc, PhandoffVc,PnewDt,PhandoffDt ]
    long double RAT2load = ratesR2.RATload();
    long double RAT3load = ratesR3.RATload();


    //**** Create array to store the states ****
    long double GvR1 = 0.0, GvR2 = 0.0, GvR3 = 0.0, Gd =0,  Hstv = 0.0, Hstva =0,  Hstvb = 0,  Hstvc = 0, HstvR1 =0,  HstvR2 = 0,  HstvR3 = 0;
    long double HstblckR1v =0,  HstblckR1d =0; //toring markov values for blocking and dropping states
    long double HstdropR1v =0,  HstdropR1d =0;
    long double HstblckR2v =0,  HstblckR2d =0;
    long double HstdropR2v =0,  HstdropR2d =0;
    long double HstblckR3v =0, HstblckR3d =0;
    long double HstdropR3v =0, HstdropR3d = 0;
    long double UR1 =0,  UR2 =0,  UR3 = 0;

    // creating arrays x.push_back("d");

     int state[6]={0,0,0,0,0,0};


    long double r1=0, r2=0, r3 =0;
//*************** class-1: VOICE SERVICES ****************************#

    //************ Admissible states & Markov SimuClation  & Call Blocking and Dropping Probabilitues *************#
    int C3 = RAT3.capacity+1;
    int T3 =RAT3.threshold +1;
    int C2 = RAT2.capacity+1;
    int T2 = RAT2.threshold+1;
    int C1 = RAT1.capacity+1;
    int T1 =RAT1.threshold+1;

    for ( int nR3v = 0;  nR3v <C3; nR3v++){
      for( int mR3v =0;  mR3v <T3; mR3v++){
        for ( int nR2v=0;nR2v <  C2; nR2v++){
          for( int mR2v =0; mR2v < T2; mR2v++){
            for ( int nR1v=0;  nR1v < C1; nR1v++){
              for( int mR1v =0;  mR1v <T1; mR1v++){

                //finding all aadmmisible states
                if ((mR1v * voice.bbu <= RAT1.threshold and (mR1v + nR1v) * voice.bbu <= RAT1.capacity) and ( mR2v*voice.bbu <= RAT2.threshold and (mR2v + nR2v)*voice.bbu <= RAT2.capacity ) and ( mR3v * voice.bbu <= RAT3.threshold and (mR3v + nR3v) * voice.bbu <= RAT3.capacity)){
                  state[0] = mR1v;
                  state[1] = nR1v;
                  state[2] = mR2v;
                  state[3] = nR2v;
                  state[4] = mR3v;
                  state[5] = nR3v;

                  /*for (int i = 5; i >= 0; i--)
                    cout << state[i] << " ";
                  cout<< "" <<endl;*/

              /*  long double  Hs = (pow(3, 10) * pow(3,6 ));
                long double Hf = ( factorial(10) * factorial(6)) ;
                long double x =Hs/Hf;
                  cout<< "Hs="<< Hs<< " * Hf="<< Hf<<" * x="<< x<<endl;*/

                //markov prossed
                  Hstva = ((pow(RAT1load, mR1v) * pow(RAT1load, nR1v)) / ( factorial(mR1v) * factorial(nR1v))) ;
                  Hstvb = ((pow(RAT2load, mR2v) * pow(RAT2load, nR2v)) / ( factorial(mR2v) * factorial(nR2v))) ;
                  Hstvc =((pow(RAT3load, mR3v) * pow(RAT3load, nR3v)) / (factorial(mR3v) * factorial(nR3v)));

                  //for RAT1
                  HstvR1 = Hstva;
                  PsR1.push_back(HstvR1);

                  //for RAT 2
                  HstvR2 = Hstva*Hstvb;
                  PsR2.push_back(HstvR2);

                  //for RAt3
                  HstvR3 = Hstva*Hstvb*Hstvc;
                  PsR3.push_back(HstvR3);


                  // calculation of the G normilisation constant
                  GvR1 += HstvR1; //Normalisation factor: addition of each state probability
                  GvR2 += HstvR2; //Normalisation factor: addition of each state probability
                  GvR3 += HstvR3; //Normalisation factor: addition of each state probability

                //  cout<< "GV  "<< Gv<<endl;
                  //cout <<" HSTV1="<< Hstv1 <<" HSTV2="<< Hstv2 <<" HSTV3="<< Hstv3<<endl;
                  //cout <<" HSTV="<< Hstv<<endl;


                  // blocking states for RAT1
                  if ((voice.bbu + mR1v * voice.bbu )> RAT1.threshold or (voice.bbu + (mR1v + nR1v) * voice.bbu) > RAT1.capacity){
                      HstblckR1v = HstblckR1v + Hstv;  // computional Markov equations
                      //blckstateR1v.push_back(state);

                      //blocking states for RAT2 must be here
                      if((voice.bbu + mR2v * voice.bbu) > RAT2.threshold or (voice.bbu + (mR2v + nR2v) * voice.bbu)  > RAT2.capacity) {
                            HstblckR2v = HstblckR2v + Hstv;  //computional Markov equations
                              //blckstateR2v.push_back(state);

                        //blocking states for RAT 3 must be here
                        if ((voice.bbu + mR3v * voice.bbu) > RAT3.threshold or (voice.bbu + (mR3v + nR3v) * voice.bbu) > RAT3.capacity){
                            HstblckR3v = HstblckR3v + Hstv; // # computional Markov equations
                            //blckstateR3v.push_back(state);
                        }
                      }
                  }

                  // Dropping states for RAT 1
                  if ((voice.bbu + (mR1v + nR1v) * voice.bbu) > RAT1.capacity){
                        HstdropR1v = HstdropR1v + Hstv; // computional Markov equations
                      // drpstateR1v.push_back(state);

                        //dropping states for RAT2
                        if ((voice.bbu + (mR2v + nR2v) * voice.bbu) > RAT2.capacity){
                          HstdropR2v = HstdropR2v + Hstv;  //computional Markov equations
                          //drpstateR2v.push_back(state);

                          //Dropping states for RAT 3
                          if ((voice.bbu + (mR3v + nR3v) * voice.bbu) > RAT3.capacity){
                            HstdropR3v = HstdropR3v + Hstv;  //computional Markov equations
                            //drpstateR3v.push_back(state);
                          }

                        }
                  }


                }



              } //inner for loop
            }
          }
        }
      }

    }

  /*  //************** Class-1: Voice probabilities *********************#
    long double NCBP1v = HstblckR1v / Gv;
    long double NCBP2v = HstblckR2v / Gv;
    long double NCBP3v = HstblckR3v / Gv;

    long double HCDP1v = HstdropR1v / Gv;
    long double HCDP2v = HstdropR2v / Gv;
    long double HCDP3v = HstdropR3v / Gv;*/


    //utilisation
    long double PstateR1;  // probability of each state
    long double PstateR2;  // probability of each state
    long double PstateR3;  // probability of each state

    for ( int nR3 = 0;  nR3 <C3; nR3++){
      for( int mR3 =0;  mR3 <T3; mR3++){
        for ( int nR2=0;nR2 <  C2; nR2++){
          for( int mR2 =0; mR2 < T2; mR2++){
            for ( int nR1=0;  nR1 < C1; nR1++){
              for( int mR1 =0;  mR1 <T1; mR1++){

                        //index to access the probabilities
                        long int n=0;
                        if(n < PsR1.size()){
                          PstateR1 = PsR1[n]/GvR1;
                        }

                        if(n < PsR2.size()){
                          PstateR2 = PsR2[n]/GvR2;
                        }

                        if(n < PsR2.size()){
                          PstateR3 = PsR3[n]/GvR3;
                        }

                        //utilisation each RAT
                        UR1 = UR1 + ((mR1 * voice.bbu + nR1 * voice.bbu) * PstateR1);
                        UR2 = UR2 + ((mR2 * voice.bbu + nR2 * voice.bbu) * PstateR2);
                        UR3 = UR3 + ((mR3 * voice.bbu + nR3 * voice.bbu) * PstateR3);
                        r1 =r1+1;
                        r2 = r2 + 1;
                        r3 =r3 + 1;

                        //Operators revenue
                        revenueR1 = revenueR1 + UR1* prbbuV;
                        revenueR2 = revenueR2 + UR2 * prbbuV;
                        revenueR3 = revenueR3 + UR3* prbbuV;
                        n+=1;

              }
            }
          }
        }
      }
    }
    PsR1.clear();
    PsR2.clear();
    PsR3.clear();

    cout<<"******************************* Class-1: Voice **********************************"<<endl;
    cout<< "" <<endl;
  //  cout<< "array size  "<< Ps.size()<<endl;

  /*  cout<<" RAT 1 New Call Blocking Probability: " << NCBP1v<<endl;
    cout<<" RAT 2 New Call Blocking Probability: "<<NCBP2v <<endl;
    cout<<" RAT 3 New Call Blocking Probability: " <<NCBP3v <<endl;
    cout<< "" <<endl;
    cout<<" RAT 1 HandOff Call Dropping Probability: " << HCDP1v<<endl;
    cout<<" RAT 2 HandOff Call Dropping Probability: "<<HCDP2v <<endl;
    cout<<" RAT 3 HandOff Call Dropping Probability: " <<HCDP3v <<endl; */
    cout<< "" <<endl;
    //cout<<"R1 R2 R3 admissible states", r1, " ", r2, " ", r3)

    long double UHWN = UR1 + UR2 + UR3;
    long double normalisedUR1 = UR1/UHWN;
    long double normalisedUR2 = UR2 /UHWN;
    long double normalisedUR3 = UR3/UHWN;

    string s1 = to_string(normalisedUR1 );
    string s2 = to_string(normalisedUR2 );
    string s3 = to_string(normalisedUR3 );

    string result  =  s1 + " "+ s2+ " " +s3+ " ";

    cout<< " normalisedUR1 "  <<  normalisedUR1 <<endl;
    cout<< "normalisedUR2 "<<normalisedUR2 <<endl;
    cout<< "normalisedUR3 " << normalisedUR3<<endl;

    return result;
    //return [normalisedUR1, normalisedUR2, normalisedUR3, revenueR1, revenueR2, revenueR3]
    //return [NCBP1v, NCBP2v , NCBP3v, HCDP1v, HCDP2v, HCDP3v, NCBP1d,  NCBP2d, NCBP3d,HCDP1d, HCDP2d, HCDP3d ]
//******************** class-1: END *********************************** #

}






int main(int argc, char* argv[]){

  cout<<"main function"<<endl;

  std::ofstream outfile;
  string split[3];

  vector<int> in;
  vector<string> result1;
  vector<string> result2;
  vector<string> result3;

  for(int i=1; i<11; i++){
      in.push_back(i);

      string r = simulator(i);
      // Used to split string around spaces.
      istringstream ss(r);
      string word; // for storing each word
      int j=0;
      while (ss >> word){
          split[j] = word;
          cout << word << "\n";
          j+=1;
      }

      //outfile.open("results.txt", std::ios_base::app); // append instead of overwrite
      //outfile << r;
      result1.push_back(split[0]);
      result2.push_back(split[1]);
      result3.push_back(split[2]);

  }

  for (int i = 0; i <in.size(); i++)
    cout << in[i] << " ";
  cout<< "" <<endl;

  for (int i = 0; i <result1.size(); i++)
    cout << result1[i] << " ";
  cout<< "" <<endl;

  for (int i = 0; i <result2.size(); i++)
    cout << result2[i] << " ";
  cout<< "" <<endl;

  for (int i = 0; i <result3.size(); i++)
    cout << result3[i] << " ";
  cout<< "" <<endl;



  outfile.close();
  return 0;
}
