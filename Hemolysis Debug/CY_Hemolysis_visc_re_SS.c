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




DEFINE_ADJUST(BD,d)
{
    Thread *c_t;
    cell_t c;
    real mu, C_mu;
    real second_invariant, re_second_invariant, tot_second_invariant;
    real tau11, tau12, tau13, tau21, tau22, tau23, tau31, tau32, tau33, tau_vm,eps_turb;
    real re_tau11, re_tau12, re_tau13, re_tau21, re_tau22, re_tau23, re_tau31, re_tau32, re_tau33, re_tau_vm;
    real tot_tau11, tot_tau12, tot_tau13, tot_tau21, tot_tau22, tot_tau23, tot_tau31, tot_tau32, tot_tau33, tot_tau_vm;
    real tau_p, tau_b, tau_eff;
    real rans_diss;

    C_mu = turb_diss_mod_const;
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
            second_invariant = fabs((tau11+tau22+tau33)*(tau11+tau22+tau33) -(tau11*tau11 + tau22*tau22 + tau33*tau33 + 2*tau12*tau21 + 2*tau23*tau32 + 2*tau13*tau31))/2;
            tau_vm = sqrt(3*second_invariant) /* fabs creates abs val of second invariant. */;
            tau_p = sqrt(second_invariant);
            tau_b = sqrt(fabs((tau11-tau22)*(tau11-tau22) + (tau11-tau33)*(tau11-tau33) + (tau22-tau33)*(tau22-tau33) + tau12*tau12 + tau13*tau13 + tau21*tau21 + tau23*tau23 + tau31*tau31 + tau32*tau32));
            /* End viscous stress calculation*/


            /* Begin reynolds stress calculation for incompressible flow */
            /* See Boussinesq eddy viscosity assumption */
            /* kroniker delta = 1 if i==j */
            re_tau11 = 2*(C_DUDX(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            re_tau22 = 2*(C_DVDY(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            re_tau33 = 2*(C_DWDZ(c,c_t))*C_MU_T(c,c_t) - 2/3*C_R(c,c_t)*C_K(c,c_t);
            re_tau12 = C_R(c,c_t)*(C_DUDY(c,c_t)+C_DVDX(c,c_t));
            re_tau13 = C_R(c,c_t)*(C_DUDZ(c,c_t)+C_DWDX(c,c_t));
            re_tau23 = C_R(c,c_t)*(C_DVDZ(c,c_t)+C_DWDY(c,c_t));
            re_tau21 = re_tau12;
            re_tau31 = re_tau13;
            re_tau32 = re_tau23;
            re_second_invariant = fabs((re_tau11+re_tau22+re_tau33)*(re_tau11+re_tau22+re_tau33) - (re_tau11*re_tau11 + re_tau22*re_tau22 + re_tau33*re_tau33 + 2*re_tau12*re_tau21 + 2*re_tau23*re_tau32 + 2*re_tau13*re_tau31))/2;
            re_tau_vm = sqrt(3*re_second_invariant) /* fabs creates abs val of second invariant. */;
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
            tot_second_invariant = fabs((tot_tau11+tot_tau22+tot_tau33)*(tot_tau11+tot_tau22+tot_tau33) - (tot_tau11*tot_tau11 + tot_tau22*tot_tau22 + tot_tau33*tot_tau33 + 2*tot_tau12*tot_tau21 + 2*tot_tau23*tot_tau32 + 2*tot_tau13*tot_tau31))/2;
            tot_tau_vm = sqrt(3*tot_second_invariant) /* fabs creates abs val of second invariant. */;
            /* End total stress calculation for incompressible flow */

            eps_turb = C_O(c,c_t)*C_K(c,c_t)*C_mu;
            tau_eff = mu*eps_turb*C_R(c,c_t);

            rans_diss = C_O(c,c_t)*C_K(c,c_t)*0.09;

            C_UDMI(c,c_t,0) = tau_vm;
            C_UDMI(c,c_t,1) = rans_diss;
            C_UDMI(c,c_t,2) = re_tau_vm;
            C_UDMI(c,c_t,3) = tot_tau_vm;
            C_UDMI(c,c_t,4) = pow(C_UDMI(c,c_t,1)*0.0035*C_R(c,c_t),.5);
            /* rans_diss correct */

            end_c_loop(c,c_t)
        }
    }
}

/* Def source terms viscous stress */
DEFINE_SOURCE(GW_visc,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,0),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,0),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_visc,c,t,dS,eqn)
{
    real C_term, Teff_term, source;

    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,0),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* Def source terms reynolds stress */
DEFINE_SOURCE(GW_reynolds,c,t,dS,eqn)
{
    real C_term, Tau_term, source;

    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,2),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,2),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_reynolds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,2),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* Def source terms total stress, visc + reynolds */
DEFINE_SOURCE(GW_tot,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,3),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,2),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_tot,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,2),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}

/* Def source terms eds */
DEFINE_SOURCE(GW_eds,c,t,dS,eqn)
{
    real C_term, Tau_term, source;
    C_term = pow(C_GW,1/beta_GW);
    Tau_term = pow(C_UDMI(c,t,4),alpha_GW/beta_GW);
    source = C_term*Tau_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(HO_eds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_HO,1/beta_HO);
    Teff_term = pow(C_UDMI(c,t,4),alpha_HO/beta_HO);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}


DEFINE_SOURCE(TZ_eds,c,t,dS,eqn)
{
    real C_term, Teff_term, source;
    C_term = pow(C_TZ,1/beta_TZ);
    Teff_term = pow(C_UDMI(c,t,4),alpha_TZ/beta_TZ);
    source = C_term*Teff_term*C_R(c,t);
    dS[eqn] = 0;
    return source;
}
