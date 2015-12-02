import creatures as c
h_head=c.bp(3000,'head',10)
h_neck=c.bp(500,'neck',5)
h_body_high=c.bp(10000,'upper body',100)
h_body_low=c.bp(10000,'lower body',90)
h_leg_high_l=c.bp(8000,'upper left leg',100)
h_leg_high_r=c.bp(8000,'upper right leg',100)
h_leg_low_l=c.bp(8000,'lower left leg',100)
h_leg_low_r=c.bp(8000,'lower right leg',100)
h_foot_l=c.bp(1000,'left foot',20)
h_foot_r=c.bp(1000,'right foot',20)
h_arm_r=c.bp(5000,'right arm',30)
h_arm_l=c.bp(5000,'left arm',30)
h_hand_r=c.bp(200,'right hand',20)
h_hand_l=c.bp(200,'left hand',20)
humanoid_body=c.Body([h_head,h_neck,h_body_high,h_body_low,h_leg_high_l,h_leg_high_r,h_leg_low_l,h_leg_low_r,h_foot_l,h_foot_r,h_arm_l,h_arm_r,h_hand_l,h_hand_r],
[
[h_head,h_neck,],
[h_neck,h_body_high],
[h_body_high,h_body_low],
[h_body_low,h_leg_high_r],
[h_body_low,h_leg_high_l],
[h_body_high,h_arm_l],
[h_body_high,h_arm_r],
[h_foot_l,h_leg_low_l],
[h_foot_r,h_leg_low_r],
[h_leg_low_l,h_leg_high_l],
[h_leg_low_r,h_leg_high_r],
[h_hand_l,h_arm_l],
[h_hand_r,h_arm_r]
])
human_race=c.Race('human','h',humanoid_body)