class RATattributes{
  public:
    int rid;
    int capacity;
    int threshold;

    RATattributes(int Rrid, int Rcapacity, int Rthreshold){
      rid = Rrid;
      capacity = Rcapacity;
      threshold = Rthreshold;

    }


};


class Services{
  public:
    int sid;
    int bbu;

    Services(int Ssid,int Sbbu){
      sid = Ssid;
      bbu = Sbbu;
    }


};


class RATloads{
  public:
    int rid;
    double arv;
    double dep;

    RATloads(int Lrid, double Larv, double Ldep){
      rid = Lrid;
      arv = Larv;
      dep = Ldep;

    }

    double RATload(void){
      return arv/dep;
    }


};
