module rt_dyn_pri_fsm ( acq_thresh_hi, acq_thresh_lo, clk, reset_n, dyn_pri, 
        dyn_update );
  input acq_thresh_hi, acq_thresh_lo, clk, reset_n;
  output dyn_pri, dyn_update;
  wire   \current_state[0] , \next_state[0] , n2, n1, n3, n4;
  assign dyn_pri = \current_state[0] ;

  dti_12g_ffqa01x1 \current_state_reg[0]  ( .D(\next_state[0] ), .CK(clk), 
        .RN(reset_n), .Q(\current_state[0] ) );
  dti_12g_ffqa11x1 dyn_update_cld_reg ( .D(n2), .CK(clk), .RN(reset_n), .SN(n1), .Q(dyn_update) );
  dti_12g_tierailx1 U3 ( .HI(n1) );
  dti_12g_muxi21xp5 U4 ( .D0(n3), .D1(acq_thresh_lo), .S(\current_state[0] ), 
        .Z(\next_state[0] ) );
  dti_12g_nor2xp13 U5 ( .A(n4), .B(\current_state[0] ), .Z(n2) );
  dti_12g_nor2xp13 U6 ( .A(dyn_update), .B(acq_thresh_hi), .Z(n4) );
  dti_12g_invxp5 U7 ( .A(acq_thresh_hi), .Z(n3) );
endmodule


module dti_voter ( in0, in1, in2, out );
  input in0, in1, in2;
  output out;
  wire   n1;

  dti_12g_aoi222rexp5 U2 ( .A1(in1), .A2(in2), .B1(in1), .B2(in0), .C1(in2), 
        .C2(in0), .Z(n1) );
  dti_12g_invxp3 U3 ( .A(n1), .Z(out) );
endmodule

