# LOL source feasibility audit

Checked UTC: 2026-09-25 01:52:07 UTC
No model was fitted and no outcome associations were calculated.

## chaincc-teams-2024.csv.gz
Rows: 20386 ; columns excluding source label: 74
Unique game IDs: 10193
Date range: 2023-08-01 15:41:50 to 2024-11-24 07:47:59
Date year counts:

 2023  2024 
  752 19634 
League counts:

            LPL             LDL            LCKC            NACL             LCK 
           1434            1130            1022             974             964 
             EM             PCL             PCS             VCS           ESLOL 
            798             680             624             614             602 
            LEC             LAS          CBLOLA           CBLOL          LVP SL 
            588             578             552             526             506 
            PRM             LFL             LLA             LCS             TCL 
            494             488             426             384             366 
           LFL2              UL           LPLOL             GLL              HM 
            358             326             320             318             318 
            EBL             LCO             NLC              AL             EPL 
            312             312             310             300             300 
            LJL             LIT            PRMP            NEXO            WLDs 
            296             274             268             264             264 
             HC             TSC             LRS             LRN              HW 
            222             214             198             176             168 
            MSI NLC Aurora Open             CDF              IC           IGNIS 
            156             154             138             136             110 
             CT           GLLPA             USP              AC           EBLPA 
             78              76              76              70              50 
            EWC             PGN 
             38              36 
Missing values in required fields:
           game_id               date             league              patch 
                 0                  0                  0                 24 
              side            team_id opponent_team_name             result 
                 0                363                  0                  0 
        gamelength           goldat10       golddiffat10         xpdiffat10 
                 0                  0                  0                  0 
        csdiffat10           goldat15       golddiffat15         xpdiffat15 
                 0                  0                  0                  0 
        csdiffat15          killsat15         deathsat15 
                 0                  0                  0 

## chaincc-teams-2025.csv.gz
Rows: 20340 ; columns excluding source label: 74
Unique game IDs: 10170
Date range: 2024-06-05 00:12:51 to 2025-12-29 10:52:27
Date year counts:

 2024  2025 
  728 19612 
League counts:

         LPL          LCK         LCKC          LAS           EM          LJL 
        1610         1110         1084          978          880          748 
         LFL          NLC          LEC          PCS          PRM           AL 
         634          628          612          606          606          584 
        NACL          LCP       LVP SL          TCL           RL         LFL2 
         554          546          530          516          480          458 
          CD         NEXO          HLL          ROL           HM           HC 
         452          430          426          416          410          400 
       LTA S        LTA N          EBL  Asia Master        LPLOL          LRN 
         388          378          372          360          344          308 
         LIT          LRS          VCS           HW         WLDs          MSI 
         302          284          282          228          192          160 
        DCup         PRMP CD Qualifier           CT        KeSPA          ASI 
         150          146          108          100           98           84 
         LTA          FST          EWC           IC           UL        ESLOL 
          80           70           66           56           32           28 
         GLL 
          26 
Missing values in required fields:
           game_id               date             league              patch 
                 0                  0                  0                  0 
              side            team_id opponent_team_name             result 
                 0                566                  0                  0 
        gamelength           goldat10       golddiffat10         xpdiffat10 
                 0                  0                  0                  0 
        csdiffat10           goldat15       golddiffat15         xpdiffat15 
                 0                  0                  0                  0 
        csdiffat15          killsat15         deathsat15 
                 0                  0                  0 

## chaincc-teams-2026.csv.gz
Rows: 18458 ; columns excluding source label: 74
Unique game IDs: 9229
Date range: 2025-07-29 15:10:01 to 2026-09-23 18:47:23
Date year counts:

 2025  2026 
  494 17964 
League counts:

         LPL          LCK         LCKC          LEC           AL          LJL 
        1348         1004          982          766          726          726 
          EM          LAS          PRM         NACL          LCP          LFL 
         662          642          624          612          602          546 
       CBLOL          ROL          LIT          HLL          LCS          EWC 
         514          514          502          486          478          464 
         EBL           RL          NLC          TCL          LES           CD 
         426          422          420          416          386          376 
         LRS          LRN           HM           HC        LPLOL           NL 
         374          352          348          338          324          274 
         VCS           HW CD Qualifier          PCS          MSI           AM 
         272          206          182          172          142          126 
   KeSPA Cup        KeSPA          FST         WSCI         CCWS        LTA S 
         122          112           90           84           80           56 
       LTA N           AC         LFL2         WLDs       LVP SL 
          48           38           30           24           20 
Missing values in required fields:
           game_id               date             league              patch 
                 0                  0                  0                  0 
              side            team_id opponent_team_name             result 
                 0                487                  0                  0 
        gamelength           goldat10       golddiffat10         xpdiffat10 
                 0                  0                  0                  0 
        csdiffat10           goldat15       golddiffat15         xpdiffat15 
                 0                  0                  0                  0 
        csdiffat15          killsat15         deathsat15 
                 0                  0                  0 

## Cross-file checks
Repeated game-side keys: 0
Rows per game:

    2 
29592 
Side codes:

 Blue   Red 
29592 29592 
Result codes:

FALSE  TRUE 
29594 29590 

## Candidate actual-date cohort: LCK LPL LEC in 2024 and 2025
Team rows: 6318
Unique games: 3159
     
      2024 2025
  LCK  964 1110
  LEC  588  612
  LPL 1434 1610
Required-field missingness:
           game_id               date             league              patch 
                 0                  0                  0                  0 
              side            team_id opponent_team_name             result 
                 0                  0                  0                  0 
        gamelength           goldat10       golddiffat10         xpdiffat10 
                 0                  0                  0                  0 
        csdiffat10           goldat15       golddiffat15         xpdiffat15 
                 0                  0                  0                  0 
        csdiffat15          killsat15         deathsat15 
                 0                  0                  0 
Patch counts:

14.01 14.02 14.03 14.04 14.05 14.06 14.10 14.11 14.12 14.13 14.14 14.15 14.16 
  388   308    96   242   296   250   132   230   134   382   212   254    62 
15.01 15.02 15.03 15.04 15.06 15.07 15.08 15.09 15.10 15.11 15.14 15.15 15.16 
  214   200   148    84   202   326   308   352   202   148   258   306   274 
15.17 15.18 
  292    18 

## Paired game validation
Noncomplementary results: 0
Zero or negative early total gold: 1522
Games ending at or before 15 minutes: 0
Nonopposite recorded differences: 0
Gold totals inconsistent with differences: 0
Any kill/death difference at 15 (not an exclusion): 30
Opposing kills exceed recorded deaths: 0
Cross-side context mismatch: 0
Nonpositive early gold by league:
     bad_early
      FALSE TRUE
  LCK  1037    0
  LEC   600    0
  LPL     0 1522
Eligible paired games: 1637
Eligible games by actual year and league:
     
      2024 2025
  LCK  482  555
  LEC  294  306
Numeric ranges:
     gamelength goldat10 goldat15 golddiffat10 golddiffat15 xpdiffat15
[1,]       1202        0        0        -3969        -8003      -6019
[2,]       3558    19068    31819         4043         8624       5625
     csdiffat15 killsat15 deathsat15
[1,]       -120         0          0
[2,]        102        14         15
