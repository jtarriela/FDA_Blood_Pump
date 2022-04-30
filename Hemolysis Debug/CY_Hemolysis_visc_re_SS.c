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

#define pi 3.1415926535897932384626433
double principal_stress(double stress_array[]);
double tresca_criterion(double stresses[]);

/* dynamic viscosity [pascal sec] */

#define turb_diss_mod_const 0.09

double principal_stress(double stress_array[]){
/* Solving characteristic cubic equation using Cardan's Method */
/* Since the stress tensor is a symmetric tensor whose elements are all real, it has real eigenvalues.
That is, the three principal stresses are real */


    /* Input array::: double stress_array[] ={tau11, tau22, tau33, tau12, tau23,tau31} */

    /* Local variable declaration */
    double p, q, D, r, I1, I2, I3, theta, sigma, sigma1, sigma2, sigma3;

    /* Invariants */
    I1 = stress_array[0] + stress_array[1] + stress_array[2];
    I2 = stress_array[0]*stress_array[1] + stress_array[1]+stress_array[2] + stress_array[0]*stress_array[2] - pow(stress_array[3],2) - pow(stress_array[4],2) - pow(stress_array[5],2);
    I3 = stress_array[0]*stress_array[1]*stress_array[2] + 2*stress_array[3]*stress_array[4]*stress_array[5] - pow(stress_array[3],2)*stress_array[2] - pow(stress_array[4],2)*stress_array[0] - pow(stress_array[5],2)*stress_array[1];

    /* p, q substitution values */
    p = I2-(I1/3);
    q = (2/27*I1)-(I1*I2/3)+I3;

    /* solve for discriminant */
    D = pow(q,2)/4 + pow(p,3)/27;
    if (D > 0){
        /* One real root, two imaginary */
        sigma = (pow(-q/2 + sqrt(D),(1/3)) + pow(-q/2 - sqrt(D),(1/3)) - I1/3);
        }
    else if (D == 0){
        /* Three real roots, two equivalent */
        sigma1 = pow(-2 * q/2, 1/3) - I1/3;
        sigma2 = pow( q/2, 1/3) - I1/3;
        double sigma[] = {sigma1, sigma2, sigma2};
        }
    else {
        /* Three real roots, unique roots */
        r = sqrt(pow(-p,3)/27);
        theta = acos(-q/2 *1/r);

        sigma1 = 2 * pow(r,1/3) * cos(theta/3) - I1/3;
        sigma2 = 2 * pow(r,1/3) * cos((2*pi+theta)/3) - I1/3;
        sigma3 = 2 * pow(r,1/3) * cos((4*pi+theta)/3) - I1/3;

        double sigma[] = {sigma1, sigma2, sigma3};
        }
    return sigma;
}

double tresca_criterion(double stresses[]){
    /* Local variable declaration */
    double tau_tresca_criterion, max1, max2;

    /* Computing maximum sigma difference */
    max1 = MAX(pow(stresses[0]-stresses[1],2), pow(stresses[1]-stresses[2]),2);
    max2 = MAX(max1, pow(stresses[0]-stresses[3]),2))
    tau_tresca_criterion = .5 * sqrt(max2);

    return tau_tresca_criterion
}

DEFINE_ADJUST(BD0,d)
{
    Thread *c_t;
    cell_t c;
    real mu;
    real tau11, tau12, tau13, tau21, tau22, tau23, tau31, tau32, tau33, tau_vm, tau_tresca, tau_blud;
    real re_tau11, re_tau12, re_tau13, re_tau21, re_tau22, re_tau23, re_tau31, re_tau32, re_tau33, re_tau_vm, re_tau_tresca, re_tau_blud;
    real tot_tau11, tot_tau12, tot_tau13, tot_tau21, tot_tau22, tot_tau23, tot_tau31, tot_tau32, tot_tau33, tot_tau_vm, tot_tau_tresca, tot_tau_blud;
    real rans_diss;
    real visc_stress_array

    /* Maximum Value functions for Tresca criteria */
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
            tau_blud = sqrt(1/3* (pow((tau11-tau22),2) + pow((tau22-tau33),2) + pow((tau33-tau11),2)) + 2*(pow(tau12,2) + pow(tau23,2)+ pow(tau31,2)));

            double visc_stress_array[] = {tau11, tau22, tau33, tau12, tau23,tau31}



            visc_prin_stress = principal_stress(Invariants_visc);
            tau_tresca = tresca_criterion(visc_prin_stress));
            /* End viscous stress calculation*/


            /* Begin reynolds stress calculation for incompressible flow */
            /* See Boussinesq eddy viscosity assumption */
            /* kroniker delta = 1 if i==j */
            re_tau11 = 2*(C_DUDX(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            re_tau22 = 2*(C_DVDY(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            re_tau33 = 2*(C_DWDZ(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            re_tau12 = C_MU_T(c,c_t)(c,c_t)*(C_DUDY(c,c_t)+C_DVDX(c,c_t));
            re_tau13 = C_MU_T(c,c_t)(c,c_t)*(C_DUDZ(c,c_t)+C_DWDX(c,c_t));
            re_tau23 = C_MU_T(c,c_t)(c,c_t)*(C_DVDZ(c,c_t)+C_DWDY(c,c_t));
            re_tau21 = re_tau12;
            re_tau31 = re_tau13;
            re_tau32 = re_tau23;
            re_tau_vm = sqrt(.5 * (pow(re_tau11-re_tau22,2) + pow(re_tau22-re_tau33,2) + pow(re_tau33-re_tau11,2)) + 3*( pow(re_tau12,2)+ pow(re_tau23,2) + pow(re_tau31,2)));
            re_tau_tresca = .5*max_3(fabs(re_tau11 - re_tau22), fabs(re_tau22-re_tau33), fabs(re_tau33-re_tau11));
            re_tau_blud = sqrt(1/3* (pow((re_tau11-re_tau22),2) + pow((re_tau22-re_tau33),2) + pow((re_tau33-re_tau11),2)) + 2*(pow(re_tau12,2) + pow(re_tau23,2)+ pow(re_tau31,2)));

            /* End reynolds stress calculation */

            /* Begin total stress calculation for incompressible flow */
            tot_tau11 = tau11 + re_tau11;
            tot_tau22 = tau22 + re_tau22;
            tot_tau33 = tau33 + re_tau33;
            tot_tau12 = tau12 + re_tau12;
            tot_tau13 = tau13 + re_tau13;
            tot_tau23 = tau23 + re_tau23;
            tot_tau21 = tau21 + re_tau21;
            tot_tau31 = tau31 + re_tau31;
            tot_tau32 = tau32 + re_tau32;
            tot_tau_vm = sqrt(.5 * (pow(tot_tau11-tot_tau22,2) + pow(tot_tau22-tot_tau33,2) + pow(tot_tau33-tot_tau11,2)) + 3*( pow(tot_tau12,2)+ pow(tot_tau23,2) + pow(tot_tau31,2)));
            tot_tau_tresca = .5*max_3(fabs(tot_tau11 - tot_tau22), fabs(tot_tau22-tot_tau33), fabs(tot_tau33-tot_tau11));
            tot_tau_blud = sqrt(1/3* (pow((tot_tau11-tot_tau22),2) + pow((tot_tau22-tot_tau33),2) + pow((tot_tau33-tot_tau11),2)) + 2*(pow(tot_tau12,2) + pow(tot_tau23,2)+ pow(tot_tau31,2)));

            /* End total stress calculation for incompressible flow */



            rans_diss = C_O(c,c_t)*C_K(c,c_t)*0.09;

            C_UDMI(c,c_t,0) = tau_vm;
            C_UDMI(c,c_t,1) = tau_tresca;
            C_UDMI(c,c_t,2) = tau_blud;
            C_UDMI(c,c_t,3) = re_tau_vm;
            C_UDMI(c,c_t,4) = re_tau_tresca;
            C_UDMI(c,c_t,5) = re_tau_blud;
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