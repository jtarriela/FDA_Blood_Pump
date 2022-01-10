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

#define C_GW_EDS .000000362
#define alpha_GW_EDS 2.416
#define beta_GW_EDS 0.785

#define C_HO_EDS 0.000000018
#define alpha_HO_EDS 1.991
#define beta_HO_EDS 0.765

#define C_TZ_EDS 0.0000001228
#define alpha_TZ_EDS 1.9918
#define beta_TZ_EDS 0.66066

#define C_EDB 0.01467
#define eps_exp 2.12

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




DEFINE_ADJUST(BloodDamage,d)
{
    Thread *c_t;
    cell_t c;
    real mu, C_mu;
    real second_invariant;
    real tau11, tau12, tau13, tau21, tau22, tau23, tau31, tau32, tau33, eps_turb;
    real tau_vm, tau_p, tau_b, tau_eff;
    real bf, mu_t_les, mu_t_rans, resolved_diss, subgrid_diss, rans_diss;

    C_mu = turb_diss_mod_const;
    thread_loop_c(c_t, d)
    {
        begin_c_loop(c,c_t)
        {
            mu =  C_MU_L(c,c_t);	/* dynamic viscosity from Carreau_Yasuda */

            tau11 = 2*(C_DUDX(c,c_t))*mu;
            tau12 = (C_DUDY(c,c_t)+C_DVDX(c,c_t))*mu;
            tau13 = (C_DUDZ(c,c_t)+C_DWDX(c,c_t))*mu;
            tau21 = tau12;
            tau22 = 2*(C_DVDY(c,c_t))*mu;
            tau23 = (C_DVDZ(c,c_t)+C_DWDY(c,c_t))*mu; tau31 = tau13;
            tau32 = tau23;
            tau33 = 2*C_DWDZ(c,c_t)*mu;
            second_invariant = fabs((tau11+tau22+tau33)*(tau11+tau22+tau33) -(tau11*tau11 + tau22*tau22 + tau33*tau33 + 2*tau12*tau21 + 2*tau23*tau32 + 2*tau13*tau31))/2;
            tau_vm = sqrt(3*second_invariant) /* fabs creates abs val of second invariant. */;
            tau_p = sqrt(second_invariant);
            tau_b = sqrt(fabs((tau11-tau22)*(tau11-tau22) + (tau11-tau33)*(tau11-tau33) + (tau22-tau33)*(tau22-tau33) + tau12*tau12 + tau13*tau13 + tau21*tau21 + tau23*tau23 + tau31*tau31 + tau32*tau32));

            /* for k-eps models: use C_D(c,t) macro */
            /* For k-omega models: convert omega to epsilon*/

            eps_turb = C_O(c,c_t)*C_K(c,c_t)*C_mu;
            tau_eff = mu*eps_turb*C_R(c,c_t);


            bf = C_STORAGE_R(c,c_t,SV_SBES_BF);
            /*mu_t_les = C_STORAGE_R(c,c_t,SV_MU_T_LES_ZONE);*/
            mu_t_les = (1-bf)*(C_MU_T(c,c_t));
            mu_t_rans = (c,c_t,SV_MU_T_SBES_RANS);

            resolved_diss = (1-bf)*pow(C_STRAIN_RATE_MAG(c,c_t),2)*0.0035/C_R(c,c_t);
            subgrid_diss = (1-bf)*pow(C_STRAIN_RATE_MAG(c,c_t),2)*mu_t_les/C_R(c,c_t);
            rans_diss = C_O(c,c_t)*C_K(c,c_t)*0.09*bf;

            C_UDMI(c,c_t,0) = tau_vm;
            C_UDMI(c,c_t,1) = rans_diss;
            C_UDMI(c,c_t,2) = subgrid_diss;
            C_UDMI(c,c_t,3) = resolved_diss + subgrid_diss + rans_diss;
            C_UDMI(c,c_t,4) = pow(C_UDMI(c,c_t,3)*0.0035*C_R(c,t),.5);
            /* subgrid_diss & resolved diss have issues */
            /* rans_diss correct */

            end_c_loop(c,c_t)
        }
    }
}
/* defining source terms for various models */
DEFINE_SOURCE(GW_model,c,t,dS,eqn)
{
    real C_term, Tau_term, source;

    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,0),alpha_GW/beta_GW);

/* C*T*rho */
    source = C_term*Tau_term*C_R(c,t);

    dS[eqn] = 0;


    return source;
}


DEFINE_SOURCE(GW_HO,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,0),alpha_HO/beta_HO);


    source = C_term*Teff_term*C_R(c,t);

    dS[eqn] = 0;

    return source;
}


/* Wu EDS */
/* Tau_eff = e_viscous_dissipation + e_turbulent_kinetic_dissipation
current model disregards viscous dissipation, fluent energy model off */

DEFINE_SOURCE(EDS_GW,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_GW_EDS,1/beta_GW_EDS);
    Teff_term = pow(C_UDMI(c,c_t,4),alpha_GW_EDS/beta_GW_EDS);

    source = C_term*Teff_term*C_R(c,t);

    dS[eqn] = 0;

    return source;
}

DEFINE_SOURCE(EDS_HO,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO_EDS,1/beta_HO_EDS);
    Teff_term = pow(C_UDMI(c,c_t,4),alpha_HO_EDS/beta_HO_EDS);

    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;

    return source;
}

DEFINE_SOURCE(EDS_TZ,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ_EDS,1/beta_TZ_EDS);
    Teff_term = pow(C_UDMI(c,c_t,4),alpha_TZ_EDS/beta_TZ_EDS);

    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;


    return source;
}

DEFINE_SOURCE(EDB,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = C_EDB;
    Teff_term = pow(C_UDMI(c,c_t,4)*0.0000001,eps_exp);

    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;


    return source;
}
