#include "udf.h"
#include<stdio.h>
#include<stdlib.h>

#define C_GW 0.0000363
#define alpha_GW 2.416
#define beta_GW 0.785

#define C_HO 0.00018
#define alpha_HO 1.991
#define beta_HO 0.765

#define C_TZ 0.00001228
#define alpha_TZ 1.9918
#define beta_TZ 0.6606

/* dynamic viscosity [pascal sec] */

#define turb_diss_mod_const 0.09


DEFINE_PROPERTY(Carreau_Yasuda,c,t)
{
    real n = 0.3568;
    real mu_cy;
    real mu_o = 0.056;
    real mu_inf = 0.0035;
    real lambda = 3.313;
    real A = 2;
    mu_cy = mu_inf+((mu_o-mu_inf)/pow((1+pow(lambda*C_STRAIN_RATE_MAG(c,t),A)),(1-n)/A));

    return mu_cy;
}


DEFINE_ADJUST(BD0,d)
{
    Thread *c_t;
    cell_t c;
    real mu;
    real tau11, tau12, tau13, tau21, tau22, tau23, tau31, tau32, tau33, tau_vm, tau_tresca, tau_blud;
    real sgs_tau11, sgs_tau12, sgs_tau13, sgs_tau21, sgs_tau22, sgs_tau23, sgs_tau31, sgs_tau32, sgs_tau33, sgs_tau_vm, sgs_tau_tsgssca, sgs_tau_blud;
    real tot_tau11, tot_tau12, tot_tau13, tot_tau21, tot_tau22, tot_tau23, tot_tau31, tot_tau32, tot_tau33, tot_tau_vm, tot_tau_tresca, tot_tau_blud;

    real rans_diss;

    /* Maximum Value functions for Tresca criteria */
    float max_3(float x, float y, float z)
    {
        return MAX(MAX(x, y), z);
    }

    thread_loop_c(c_t, d)
    {
        begin_c_loop(c,c_t)
        {
            mu =  C_MU_L(c,c_t);

            /* Begin viscous stress calculation */
            tau11 = 2*(C_DUDX(c,c_t))*mu;
            tau12 = (C_DUDY(c,c_t)+C_DVDX(c,c_t))*mu;
            tau13 = (C_DUDZ(c,c_t)+C_DWDX(c,c_t))*mu;
            tau21 = tau12;
            tau22 = 2*(C_DVDY(c,c_t))*mu;
            tau23 = (C_DVDZ(c,c_t)+C_DWDY(c,c_t))*mu;
            tau31 = tau13;
            tau32 = tau23;
            tau33 = 2*C_DWDZ(c,c_t)*mu;

            tau_vm = sqrt(.5 *(pow(tau11-tau22,2) + pow(tau22-tau33,2) + pow(tau33-tau11,2)) + 3*( pow(tau12,2)+ pow(tau23,2) + pow(tau31,2)));
            tau_tresca = .5*max_3(fabs(tau11 - tau22), fabs(tau22-tau33), fabs(tau33-tau11));
            tau_blud = sqrt(1/3* (pow((tau11-tau22),2) + pow((tau22-tau33),2) + pow((tau33-tau11),2)) + 2*(pow(tau12,2) + pow(tau23,2)+ pow(tau31,2)));
            /* End viscous stress calculation*/


            /* Begin subgrid stress calculation for incompressible flow */
            /* See Boussinesq eddy viscosity assumption */
            /* kroniker delta = 1 if i==j */
            sgs_tau11 = 2*(C_DUDX(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            sgs_tau22 = 2*(C_DVDY(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            sgs_tau33 = 2*(C_DWDZ(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            sgs_tau12 = C_MU_T(c,c_t)(c,c_t)*(C_DUDY(c,c_t)+C_DVDX(c,c_t));
            sgs_tau13 = C_MU_T(c,c_t)(c,c_t)*(C_DUDZ(c,c_t)+C_DWDX(c,c_t));
            sgs_tau23 = C_MU_T(c,c_t)(c,c_t)*(C_DVDZ(c,c_t)+C_DWDY(c,c_t));
            sgs_tau21 = sgs_tau12;
            sgs_tau31 = sgs_tau13;
            sgs_tau32 = sgs_tau23;
            sgs_tau_vm = sqrt(.5 * (pow(sgs_tau11-sgs_tau22,2) + pow(sgs_tau22-sgs_tau33,2) + pow(sgs_tau33-sgs_tau11,2)) + 3*( pow(sgs_tau12,2)+ pow(sgs_tau23,2) + pow(sgs_tau31,2)));
            sgs_tau_tresca = .5*max_3(fabs(sgs_tau11 - sgs_tau22), fabs(sgs_tau22-sgs_tau33), fabs(sgs_tau33-sgs_tau11));
            sgs_tau_blud = sqrt(1/3* (pow((sgs_tau11-sgs_tau22),2) + pow((sgs_tau22-sgs_tau33),2) + pow((sgs_tau33-sgs_tau11),2)) + 2*(pow(sgs_tau12,2) + pow(sgs_tau23,2)+ pow(sgs_tau31,2)));

            /* End reynolds stress calculation */

            /* Begin total stress calculation for incompressible flow */
            tot_tau11 = tau11 + sgs_tau11;
            tot_tau22 = tau22 + sgs_tau22;
            tot_tau33 = tau33 + sgs_tau33;
            tot_tau12 = tau12 + sgs_tau12;
            tot_tau13 = tau13 + sgs_tau13;
            tot_tau23 = tau23 + sgs_tau23;
            tot_tau21 = tau21 + sgs_tau21;
            tot_tau31 = tau31 + sgs_tau31;
            tot_tau32 = tau32 + sgs_tau32;
            tot_tau_vm = sqrt(.5 * (pow(tot_tau11-tot_tau22,2) + pow(tot_tau22-tot_tau33,2) + pow(tot_tau33-tot_tau11,2)) + 3*( pow(tot_tau12,2)+ pow(tot_tau23,2) + pow(tot_tau31,2)));
            tot_tau_tresca = .5*max_3(fabs(tot_tau11 - tot_tau22), fabs(tot_tau22-tot_tau33), fabs(tot_tau33-tot_tau11));
            tot_tau_blud = sqrt(1/3* (pow((tot_tau11-tot_tau22),2) + pow((tot_tau22-tot_tau33),2) + pow((tot_tau33-tot_tau11),2)) + 2*(pow(tot_tau12,2) + pow(tot_tau23,2)+ pow(tot_tau31,2)));

            /* End total stress calculation for incompressible flow */



            rans_diss = C_O(c,c_t)*C_K(c,c_t)*0.09;

            C_UDMI(c,c_t,0) = tau_vm;
            C_UDMI(c,c_t,1) = tau_tresca;
            C_UDMI(c,c_t,2) = tau_blud;
            C_UDMI(c,c_t,3) = sgs_tau_vm;
            C_UDMI(c,c_t,4) = sgs_tau_tresca;
            C_UDMI(c,c_t,5) = sgs_tau_blud;
            C_UDMI(c,c_t,6) = tot_tau_vm;
            C_UDMI(c,c_t,7) = tot_tau_tresca;
            C_UDMI(c,c_t,8) = tot_tau_blud;
            C_UDMI(c,c_t,9) = pow(C_UDMI(c,c_t,1)*0.0035*C_R(c,c_t),.5);
            C_UDMI(c,c_t,10) = rans_diss;
            /* rans_diss correct */

            end_c_loop(c,c_t)
        }
    }
}

/* --------------------------------------------------------------------------------- */
/* Def source terms eds */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_eds,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,9),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_eds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,9),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_eds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,9),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def VM source terms viscous stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_vm_visc,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,0),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_vm_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,0),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_vm_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,0),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def VM source terms reynolds stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_vm_reynolds,c,t,dS,eqn)
{
    real C_term, Tau_term, source;

    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,3),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_vm_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,3),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_vm_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,3),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def VM source terms total stress, visc + reynolds */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_vm_tot,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,6),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_vm_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,6),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_vm_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,6),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def Tresca source terms viscous stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_tr_visc,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,1),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_tr_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,1),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_tr_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,1),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


/* --------------------------------------------------------------------------------- */
/* Def Tresca source terms reynolds stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_tr_reynolds,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,4),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_tr_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,4),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_tr_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,4),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def Tresca source terms total stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_tr_tot,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,7),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_tr_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,7),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_tr_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,7),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def Bludszuweit source terms viscous stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_b_visc,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,2),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_b_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,2),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_b_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,2),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* --------------------------------------------------------------------------------- */
/* Def Bludszuweit source terms reynolds stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_b_reynolds,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,5),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_b_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,5),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_b_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,5),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


/* --------------------------------------------------------------------------------- */
/* Def Bludszuweit source terms total stress */
/* --------------------------------------------------------------------------------- */
DEFINE_SOURCE(GW_b_tot,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,8),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_b_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,8),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_b_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,8),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}