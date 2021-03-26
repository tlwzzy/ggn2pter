import requests
import re
from bs4 import BeautifulSoup
import os
import scatfunc
import json
import bencodepy
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
pter_key = config['PASSKEY']['pter_key']
torrent_dir = config['WORKDIR']['torrent_dir']
scene_list = ['0Saft', '0x0007', '0x0008', '0x0815', '1C', '1KING', '1UP', '1way', '20', '2006', '2CH', '2DB', '2GCREW',
              '2TU', '30', '313', '320', '3DiSO', '404', '41ST', '420Ripz', '4DiAMONDS', '4FuN', '4HM', '55L', '6rz',
              '8088', '97', 'AAoCG', 'ABEZMP3', 'ABGEKACKT', 'ABSENCE', 'ABSENTiA', 'ABSOKT', 'ABSTRAKT', 'ACC',
              'ACCiDENT', 'ACE', 'ACME', 'ACR', 'ACTiVATED', 'ACTiViSiON', 'ADDICTION', 'ADDONiA', 'ADM', 'ADVANCE',
              'AEC', 'AES', 'AF', 'AFO', 'AFT', 'AFi', 'AGAiN', 'AGS', 'ALMoST', 'ALPMP3', 'ALiAS', 'ALiEN', 'AMNESiA',
              'AMOK', 'AMPED', 'AMRC', 'AMRCMPG', 'AMX', 'ANOMALY', 'ANTiDOTE', 'ANY', 'ANiMP3', 'ANiPUNK', 'APATHY',
              'APPSiDERS', 'ARM', 'ARMADA', 'ARNDOX', 'ARROGANCE', 'ARROGANE', 'ARTiSAN', 'ASG', 'ASGARD', 'ASTYLE',
              'ATAX', 'ATF', 'ATM', 'ATONEMENT', 'ATR', 'ATX', 'AUD', 'AVENGED', 'AW', 'AWSK', 'AXiS', 'Abuse',
              'AcapeLLa', 'AdvancePower', 'AiRISO', 'Allstars', 'AnA', 'AoC', 'Astray', 'B2R', 'BACARDI', 'BACKLASH',
              'BADBOYS', 'BAHAMUT', 'BAKA', 'BALTHAZAR', 'BAT', 'BAZOOKA', 'BB', 'BBM', 'BBX', 'BCC', 'BELiN', 'BERC',
              'BERRYPDA', 'BEX', 'BF', 'BFHMP3', 'BHTPS3', 'BLA', 'BLADERUNNERS', 'BLG', 'BLT', 'BLUERAY', 'BLZPDA',
              'BLZTiK', 'BLeH', 'BMDOX', 'BMI', 'BMOC', 'BMP', 'BOLT', 'BOOLZ', 'BOS', 'BOSS', 'BPM', 'BPM_HOUSE',
              'BRAIN', 'BRD', 'BREEZE', 'BReWErS', 'BSC', 'BURGER', 'BUTT', 'BUdD', 'BWA', 'BWA_knk', 'BaTmAnN',
              'Balthazar', 'Bamboocha', 'BbP', 'BiM', 'BiOSHOCK', 'BiTE', 'BigBlueBox', 'BkW', 'BlaZe', 'BlackBOX',
              'BleH', 'BluePrint', 'BnL', 'C4', 'CACOLAC', 'CALIBUR', 'CALLOFDOODY', 'CALiSO', 'CANDYISO', 'CANDYiSO',
              'CANNABiS', 'CAPS', 'CARBON', 'CCCLX', 'CDZ', 'CEC', 'CELEBRE', 'CENTURY', 'CERTiSO', 'CEZAR', 'CFB',
              'CFD', 'CFF', 'CFT', 'CHARGED', 'CHATO', 'CHEATERS', 'CHICNCREAM', 'CHR', 'CHRONIC', 'CHRONiC', 'CHaWiN',
              'CHiC', 'CHwDgB', 'CI', 'CIY', 'CLANDESTINE', 'CLANDESTiNE', 'CLARE', 'CLASS', 'CLASSICS', 'CLASSiC',
              'CLASSiO', 'CLEAR', 'CLICK', 'CLMDOX', 'CLR', 'CLS', 'CLaSSiCs', 'CMG', 'CMP', 'CMS', 'CMT', 'CNBS',
              'CNS', 'COBO', 'COCMP3', 'COD', 'CODEPUNKS', 'CODEX', 'COGENT', 'COLLATERAL', 'COM', 'COMPLEX',
              'CONCERNED', 'CONFLiCT', 'CONFUSION', 'CONJUNKS', 'CONSOLE', 'CONSPIR4CY', 'CONTRAST', 'CONTiNUE',
              'CONVICTION', 'CONViCTiON', 'CONZ', 'COPS', 'COR', 'CORE', 'COREPDA', 'CORiSO', 'COS', 'COiSo', 'CPL',
              'CPS', 'CPY', 'CQi', 'CR', 'CRACKROX', 'CRD', 'CRDPDA', 'CREDiTWHORES', 'CRIME', 'CRL', 'CRN',
              'CROSSFiRE', 'CRP', 'CRSmp3', 'CRT', 'CRUELTY', 'CSISO', 'CSR', 'CSiS', 'CSiSO', 'CTA', 'CUBESOFT',
              'CURSED', 'CUSA', 'CVSiSO', 'CYGiSO', 'CZN', 'CaF', 'CaHeSo', 'CandyISO', 'Caravan', 'Carbon', 'CaviaR',
              'CaviaRiSO', 'ChIP4FRiENDS', 'ChaSe', 'Chakk', 'Chakky', 'Chameleon', 'Chato', 'Chikan', 'Chorro',
              'Chr0mE', 'Chronic', 'CiA', 'CiFE', 'CiG', 'CiNEMiNi', 'ConFuSiON', 'CoolPoint', 'Crokk', 'Cryotik',
              'Cyclone', 'CzW', 'D3Si', 'DAF', 'DAGGER', 'DAMNATION', 'DANAROX', 'DARKFORCE', 'DARKLiGHT', 'DARKNeZZ',
              'DARKSiDERS', 'DARKZER0', 'DARWiN', 'DAW', 'DC', 'DCP', 'DCPS', 'DCS', 'DComics', 'DD', 'DDB', 'DDC',
              'DDD', 'DDS', 'DDZ', 'DDumpers', 'DE', 'DEATH', 'DEATHCUBE', 'DEF', 'DEFA', 'DEFECT', 'DEFENSE', 'DELTA',
              'DELiGHT', 'DETONATiON', 'DEVIANCE', 'DEVOTiONS', 'DEViANCE', 'DEViANCEKennedy', 'DEZ', 'DF', 'DFG',
              'DFL', 'DFT', 'DGN', 'DHS', 'DIE', 'DIGAMES', 'DINOByTES', 'DISCREET', 'DIVINE', 'DIY', 'DJ', 'DLS',
              'DLT', 'DMAiSO', 'DMG', 'DMT', 'DMU', 'DN', 'DNB', 'DNC', 'DNL', 'DOC', 'DOCTRiNE', 'DOD', 'DOGE',
              'DOGMA', 'DOH', 'DOL', 'DOLLHEAD', 'DOLMEXICA', 'DON', 'DOSENPfAND', 'DPS', 'DQM', 'DRASTIC',
              'DROiDRAGEPDA', 'DRUNK', 'DRabbits', 'DSG', 'DSP', 'DSRP', 'DST', 'DSperate', 'DTA', 'DTC', 'DTSISO',
              'DUHPiSO', 'DUMPER', 'DUPLEX', 'DUREX', 'DV', 'DVCON', 'DVN', 'DVNISO', 'DVNMP3', 'DVNiSO', 'DVTPDA',
              'DVX', 'DW', 'DWP', 'DX', 'DYNAMiCS', 'DYNAMiTE', 'DYNASTY', 'DarKmooN', 'DarkSide', 'DeBTPDA',
              'Deviance', 'DiGiTALMAN', 'DiM', 'DiMiTRY', 'DiNOBYTES', 'DiPLODOCUS', 'DiSASTER', 'DiZZy', 'DoNuT',
              'Dosenpfand', 'DownLink', 'Downlink', 'DpR', 'DrDOX', 'DrXBOX', 'DrastiC', 'DsR', 'DvB', 'Dynarox',
              'ECHELON', 'ECZ', 'ED', 'EDF', 'EDiT', 'EG', 'EGM', 'EGO', 'EKO', 'ELEGANCE', 'EMBRACE', 'EML', 'EMP',
              'EMPORiO', 'EMiNENT', 'ENDOR', 'ENERGY', 'ENLIGHT', 'ENVY', 'ENiGMA', 'ENiGMACONSOLE', 'EOD', 'EOS',
              'EOSiNT', 'EP', 'EPH', 'EPSYLON', 'EPiSODE', 'ERGO', 'ESAD', 'ESC', 'ESI', 'ESK', 'ESP', 'EST', 'ESTEEM',
              'ETA', 'ETERNITY', 'ETH0', 'ETHNiC', 'ETM', 'ETY', 'EU', 'EUR', 'EURASIA', 'EURASiA', 'EVASION',
              'EVIGHET', 'EViLISO', 'EViLiSO', 'EWA', 'EXCALIBUR', 'EXP', 'EXTRAS', 'EXiMiUS', 'EZGAME', 'Eclipse2k',
              'EdN', 'EiTheL', 'EiTheLMP3', 'EiTheLiSO', 'EnDoR', 'EnvY', 'ErES', 'Error403', 'Ety', 'Euphoria', 'EviL',
              'EwA', 'F2L', 'F34R', 'F4CG', 'F4G', 'FA', 'FAGLIGHT', 'FAGiSO', 'FAKE', 'FAM', 'FANAiON', 'FANiSO',
              'FAS', 'FASDOX', 'FASiSO', 'FBI', 'FBiSO', 'FCC', 'FCN', 'FEA', 'FEGEFEUER', 'FERNETiSO', 'FESTiS',
              'FEZMP3', 'FFF', 'FIGHTCLUB', 'FINDME', 'FJG', 'FKK', 'FLA', 'FLT', 'FLTDOX', 'FM', 'FMC', 'FORCE',
              'FORFRIENDS', 'FRM', 'FROGS', 'FRP', 'FRiENDS', 'FRiENDs', 'FRiHET', 'FSO', 'FSP', 'FSPViDZ', 'FST',
              'FTD', 'FTF', 'FTFDOX', 'FTFiSO', 'FTH', 'FTV', 'FUA', 'FUCT', 'FULL', 'FYK', 'FaiLEDPDA', 'Fari',
              'FastSCeNe', 'Faster1948', 'FiGHTCLUB', 'FiH', 'FiRM', 'FireX', 'FnaC', 'FrEE', 'FuFFENS', 'FuGLi',
              'FuSeD', 'FuZZLe', 'G1R0cKzPDA', 'G3L', 'GAC', 'GAD', 'GAME', 'GAMEOVER', 'GAMERZ', 'GANT', 'GANTiSO',
              'GBA', 'GBANOW', 'GBANow', 'GBATemp', 'GBAnow', 'GBL', 'GBN', 'GBT', 'GBX', 'GBXR', 'GC', 'GCM', 'GCP',
              'GCS', 'GENESIS', 'GESPIELT', 'GFISO', 'GFORCE', 'GFZPS2', 'GGS', 'GHB', 'GHC', 'GHS', 'GLORY', 'GLoBAL',
              'GM', 'GME2000', 'GMG', 'GMiSO', 'GNS', 'GNSDOX', 'GOD', 'GOGoMaNiaK', 'GOODLIFE', 'GOREHOUNDS',
              'GOREPSP', 'GOV', 'GOW', 'GP', 'GPPS', 'GPSP', 'GPU', 'GR', 'GRATIS', 'GRATiS', 'GREY', 'GRI', 'GRN',
              'GRP', 'GRW', 'GRiDLOCK', 'GRiSO', 'GS', 'GSXR', 'GUiDANCE', 'GWL', 'GWViD', 'GXBG', 'GXC', 'GXE',
              'GZONE', 'GalenMyra', 'GameStop', 'GeNiuS', 'Genius', 'Ghost', 'GiRLiSO', 'GiSO', 'GloBAL', 'Global',
              'GoLD', 'GoRoNu', 'Googlecus', 'Goomba', 'GxTV', 'H3X', 'H4X', 'H5N1', 'H5N1x', 'HADOUKEN', 'HATEDOX',
              'HATRED', 'HAVOC', 'HAZARD', 'HB', 'HBD', 'HBLiVE', 'HCU', 'HDFRiENDs', 'HDP', 'HERiTAGE', 'HFT',
              'HHKids', 'HHT', 'HI2U', 'HM', 'HOBiO', 'HOLYCUBE', 'HOMERUN', 'HOODLUM', 'HOOLIGANS', 'HOOLiGANS',
              'HQEM', 'HR', 'HRS', 'HS', 'HSA', 'HSACLASSiX', 'HSALIVE', 'HTB', 'HTF', 'HUPO', 'HV', 'HYBRID', 'HYBRiD',
              'HYP', 'HYPERION', 'HYPERiON', 'HaZMaT', 'HandHeld', 'HandHeldXXX', 'HiDDEN', 'HiRE', 'HiT2000', 'HkM',
              'HkMtV', 'Homely', 'HooD', 'Hooligans', 'Hybrid', 'Hyperion', 'ICE', 'ICP', 'IFC', 'IHDC', 'ILL',
              'IMPERIAL', 'IMSDOX', 'IMT', 'IMs', 'INC', 'IND', 'INT', 'INTERGANG', 'INd', 'IRQ', 'ISO', 'ISoWoRLD',
              'IT', 'ITA', 'ITZ', 'I_KnoW', 'Intergang', 'Isolation', 'JAFFA', 'JAGDOX', 'JAGUAR', 'JAGiSO', 'JAH',
              'JAM', 'JBL', 'JCE', 'JCT', 'JEDi', 'JEDiDOX', 'JEI', 'JESTERS', 'JFK', 'JFKPC', 'JGTiSO', 'JOiNT',
              'JPMORGAN', 'JRGS', 'JRP', 'JRP_INT', 'JURAI', 'JiM', 'JiOO', 'JoWooD', 'JoWood', 'JuNGLEFeVER', 'Jurai',
              'KALISTO', 'KANiMOGE', 'KARHU', 'KC', 'KFC', 'KFKiSO', 'KICKASS', 'KINKYSEXBOX', 'KLF', 'KLOTEKLAPPERS',
              'KOMA', 'KORV', 'KOTF', 'KOUALA', 'KREMA', 'KSi', 'KTMP3', 'KUMA', 'KYR', 'Kalisto', 'KiMERA', 'KiOSK',
              'KileyNBeagle', 'Kirin', 'KoKiRi', 'KrbZ', 'KuDoS', 'KzT', 'L0sMaN0L0S', 'L0sMan0l0s', 'L2M', 'L4M3RS',
              'LALA', 'LAME', 'LAMERS', 'LBP', 'LCS', 'LEGEND', 'LEGENDS', 'LF', 'LFC', 'LGC', 'LIGHTFORCE', 'LMRYiSO',
              'LMi', 'LND', 'LOADER', 'LOADiNG', 'LOGOS', 'LOKi', 'LOL', 'LOOM', 'LOONYCUBE', 'LOVE', 'LS', 'LTB',
              'LUBE', 'LUMA', 'LUNDOX', 'LaKiTu', 'Label', 'LameFuck', 'LamerX', 'Legends', 'LiBERTY', 'LiBRiCiDE',
              'LiBiSO', 'LiGHTFORCE', 'LiNKLE', 'LiNk', 'LiPToN', 'LiR', 'LiTE', 'LiTHiUM', 'LiThIuM', 'LiViTY',
              'LoCAL', 'LoD', 'Ltd', 'Lube', 'Luna', 'LyRA', 'Lz0', 'Lz0PDA', 'LzY', 'M3', 'M3F', 'MAC', 'MACK4',
              'MACiSO', 'MAD', 'MAFiA', 'MAGBUSTERS', 'MAJiK', 'MARVEL', 'MAXiNN', 'MAZE', 'MBI', 'MCA', 'MCO', 'MDT',
              'ME', 'MESH', 'META', 'METHS', 'MFD', 'MFMP3', 'MFN', 'MFU', 'MINCHOU', 'MIRACLE', 'MK2', 'MKN', 'MM',
              'MNC', 'MNS', 'MOBLISS', 'MOD', 'MODE7', 'MOEMOE', 'MOGE', 'MOJiTO', 'MOLEIA', 'MOMENT', 'MONCUL',
              'MONEY', 'MOONCUBE', 'MOONWALKER', 'MOVE', 'MPX', 'MRDR', 'MRGL', 'MRN', 'MS', 'MSD', 'MSDC', 'MSFTUG',
              'MSGPDA', 'MSRP', 'MST', 'MUGS', 'MUPS2S', 'MUPSP', 'MUSiQ', 'MUX360S', 'MV', 'MYCEL', 'MYTH', 'MaXXiM',
              'MainichiHentaiShimbun', 'MarKes', 'MarvTM', 'MaxG', 'McDonalds', 'MeLA', 'Megaroms', 'Metroid', 'Mi',
              'MiM', 'MiNERAL', 'MiNT', 'MiP', 'MiRACLE', 'MiRC', 'MiRROR', 'MiS', 'MiT', 'Mirage', 'MnD', 'MoB',
              'MoDu', 'MoNGoLS', 'MoOSE', 'Mode7', 'MorningWood', 'MrClean', 'MrT', 'MvM', 'NACOSTEAM', 'NAGGERS',
              'NAPALM', 'NAPT', 'NAR', 'NAWAK', 'NBC', 'NBD', 'NBS', 'NCC', 'NDP', 'NDT', 'NEET', 'NEREiD', 'NESSUNO',
              'NETSHOW', 'NEXUS', 'NFA', 'NFC', 'NFL', 'NG', 'NGEN', 'NLiSO', 'NMS', 'NO', 'NOBODY', 'NOKiA', 'NOMiS',
              'NONEEDPDX', 'NONFO', 'NOTICE', 'NOW', 'NOY', 'NOiR', 'NOiSE', 'NRP', 'NXS', 'NYD', 'Navarac', 'NdsBbs',
              'Netshow', 'NexGruV', 'NextLevel', 'NextLevelPSXPSP', 'NgM', 'NiAR', 'NiG', 'NiTRO', 'NiiNTENDO',
              'NoRRNet', 'Nocturnal', 'NotMulti', 'NrZ', 'NuCVCD', 'NuHS', 'NukeThis', 'NumbNutz', 'O2', 'OASiS',
              'OBLiViON', 'OBiT', 'OE', 'OGC', 'OGN', 'OGV', 'OGViDz', 'OHM', 'OKTAN', 'OM', 'OMGba', 'OND', 'ONDSKAB',
              'ONe', 'OPIUM', 'ORANGE', 'ORGASM', 'ORIGIN', 'OS', 'OS12s', 'OSC', 'OSM', 'OSR', 'OSX', 'OTL', 'OUTCAST',
              'OUTLAWS', 'OWI', 'OZM', 'ObP', 'Oldschool', 'OneUp', 'OneUp_iNT', 'OpR', 'Open360', 'Orgasm', 'Otakon',
              'Ouzo', 'P.I.M.P', 'P2C', 'P2PSAURUS', 'PACT', 'PAL', 'PARACOX', 'PARADISO', 'PARADOX', 'PARADiGM',
              'PARADiSO', 'PARAGON', 'PARANOiD', 'PATCHWORK', 'PATIENCE', 'PATIENTZ', 'PATiENCE', 'PCD', 'PCGAME', 'PD',
              'PDC', 'PDG', 'PDM', 'PDMiSO', 'PDX', 'PE', 'PEEPSHOW', 'PEE_ES_PEE', 'PEKET', 'PEMA', 'PENTAGRAM',
              'PENiS', 'PEPiTO', 'PERVERSiON', 'PETANK', 'PGS', 'PH', 'PHX', 'PHXiSO', 'PI', 'PIEP', 'PIMP', 'PKR',
              'PLATiN', 'PLAY', 'PLAYASiA', 'PLAYME', 'PLAYTHIS', 'PLAYiT', 'PLAZA', 'PLEX', 'PLUS3DS', 'PM', 'PMM',
              'PMR', 'PMS', 'PMSx', 'PNX', 'POE', 'POLEliTE', 'POLLA', 'POP', 'POPSTATION', 'POPUP', 'PORNOLATiON',
              'PORTABLE', 'POSTMORTEM', 'PPTCLASSiCS', 'PR', 'PRALiEN', 'PRD', 'PRECiSiON', 'PREDoMiNANT', 'PRELUDE',
              'PRENDSMOi', 'PRESTIGE', 'PRESTiGE', 'PRIZM', 'PRO', 'PROCYON', 'PROFUSiON', 'PROFiT', 'PROJECTG',
              'PROJECTX', 'PROMiNENT', 'PROOF', 'PROPAGE', 'PROPHET', 'PROST', 'PROTOCOL', 'PROTON', 'PROVISION',
              'PROViSiON', 'PRS', 'PRiZM', 'PS2', 'PS2CHIMPS', 'PS2CHUMPS', 'PS2DVD', 'PS3-JRP', 'PS4GEN', 'PSD',
              'PSFR33', 'PSG', 'PSIII', 'PSN', 'PSP', 'PSPCYN', 'PSPKiNG', 'PSPLAYON', 'PSPNFO', 'PSPStick', 'PSPTV',
              'PSX', 'PSY', 'PSiCO', 'PT', 'PTC', 'PTG', 'PTL', 'PTM', 'PULSAR', 'PULSE', 'PUPPA', 'PUSSYCAT', 'PUX',
              'PWR', 'PWZ', 'PWZISO', 'PWZiSO', 'PYM', 'PYR', 'PYRiDiA', 'PaL', 'PaYNE', 'Patience', 'PhaseZero',
              'PiEISO', 'PiKMiN', 'PiL', 'PiNDASAUS', 'PiONEER', 'PiRG', 'PiT', 'PiTTs', 'PiXeL', 'PiZZA', 'PiZZADOX',
              'PirateK', 'Playable', 'Playdox', 'PmV', 'PoS', 'PoWeRUp', 'PrUtSers', 'PreCiSiON', 'ProCiSiON',
              'Project', 'ProjectG', 'ProjectX', 'ProjextX', 'PsPViD', 'PsPluS', 'PsPlus', 'PsyCZ_NP', 'PulSar',
              'Px777', 'QK', 'QKE', 'QLiMAX', 'QLiMAXDOX', 'QMB', 'QMD', 'QMI', 'QSR', 'QTXMp3', 'QUANTiZE', 'QUARTEX',
              'QUASAR', 'QUBiSM', 'Quartex', 'QuiZ', 'QwiiF', 'R0CK', 'R18', 'R2', 'R3', 'R3D', 'RABO', 'RADIAN',
              'RADiANCE', 'RAGEMP3', 'RAM', 'RANT', 'RAPTURE', 'RAPiD', 'RARE', 'RARNeT', 'RARNeTDOX', 'RAS', 'RAY',
              'RAZOR', 'RAZOR1911', 'RAZORCD', 'RAZORDOX', 'RAZoRDOX', 'RAiDiSO', 'RAiN', 'RAiNpda', 'RC', 'RDA', 'RDG',
              'RDU', 'REACT0R', 'REAL', 'REALM', 'REBORN', 'RECHARGED', 'REDUX', 'REEXIT', 'REFLEX', 'REFLUX', 'REGiON',
              'RELOADED', 'RELOADEDKENNEDY', 'RELOADEDSISTERS', 'REMiX', 'REQ', 'RES', 'RESPAWN', 'RETRiBUTiON', 'REV',
              'REV0', 'REVENGE', 'REVOLUTiON', 'RFD', 'RFL', 'RFTD', 'RHI', 'RHYTHMIC', 'RINDVIEH', 'RIOT', 'RIZN',
              'RKS', 'RLT', 'RLX', 'ROCKET', 'ROD', 'ROM', 'ROR', 'RPF', 'RPG', 'RR', 'RRR', 'RRoD', 'RS', 'RSD', 'RSE',
              'RSISO', 'RST', 'RSiSO', 'RTB', 'RTC', 'RTN', 'RTNiSO', 'RTP', 'RUNE', 'RUNUMD', 'RUSiSO', 'RVL', 'RVM',
              'RWE', 'RX', 'RYOUZANPAKU', 'RYiSO', 'RZR', 'RaZaDoO', 'Razor', 'Razor1911', 'RazorDOX', 'RazorDoX',
              'RazorDox', 'ReAZOn', 'ReFluX', 'ReForM', 'ReG', 'ReGiT', 'ReJecTS', 'ReUnion', 'ReVOLT', 'ReVOLVeR',
              'ReVPSP', 'ReVeRse', 'Recycled', 'RedT', 'ReeBSaW', 'Reloaded', 'RiCiN', 'RiKSKRiM', 'RiOT', 'RiP',
              'RiSCiSO', 'RiSO', 'RiTUEL', 'RiZ', 'RiZN', 'Riot', 'RoME', 'RobotKillers', 'Rocket', 'Romar', 'RpM',
              'RtB', 'SACRED', 'SAFTPRESSE', 'SAGE', 'SAVAGE', 'SAW', 'SC', 'SCANDiC', 'SCE', 'SCENENOTICE', 'SCOTCH',
              'SCP', 'SCRABBLE', 'SCRAM', 'SCT', 'SCZ', 'SCaNS', 'SCiENCE', 'SDA', 'SDC', 'SDM', 'SDR', 'SDS', 'SE',
              'SECRETDOOR', 'SECURITY', 'SECiSO', 'SELECT', 'SEVER', 'SEvEN', 'SFA', 'SGE', 'SHOCKBiO', 'SHOCKiSO',
              'SHOGUN', 'SHOT', 'SHiBUYA', 'SHiTONLYGERMAN', 'SI', 'SIGNUM', 'SKIDROW', 'SKL', 'SKOGOZ', 'SKY',
              'SKYFiSH', 'SKiDROW', 'SKiLL', 'SKiTFiSKE', 'SL', 'SLT', 'SLV', 'SLaM', 'SMA', 'SMACKs', 'SMD06', 'SMF',
              'SMO', 'SMP', 'SMS', 'SMeG', 'SMiD', 'SMuT', 'SND', 'SNR', 'SNiKMP3', 'SOF', 'SOM', 'SORK', 'SOULX', 'SP',
              'SPARE', 'SPECTER', 'SPHINX', 'SPHiNX', 'SPIRO', 'SPLATTER', 'SPLATTERKiNGS', 'SPLiFF', 'SPLiT',
              'SPOTLiGHT', 'SPQR', 'SPT', 'SPiCE', 'SPiN', 'SPiRiT', 'SPiTFiRE', 'SQ', 'SQL', 'SQUARE', 'SQUiRE', 'SR',
              'SRG', 'SRM', 'SRP', 'SSR', 'ST0N3D', 'STALLiON', 'STAR', 'STARCUBE', 'STATUS', 'STATiC', 'STAiSO', 'STD',
              'STEAMPUNKS', 'STINKYCUBE', 'STORMAN', 'STRANGE', 'STRESS', 'STRIKE', 'STRS', 'STRiKE', 'SUBTiLE',
              'SUCCESSiON', 'SUG', 'SUNSHiNE', 'SUPREMACY', 'SURPLUS', 'SUSHi', 'SUSU', 'SUT', 'SUXXORS', 'SUiCiDE',
              'SVENNE', 'SWAG', 'SWE', 'SWE6RUS', 'SWiFT', 'SYNDiCATE', 'SaNdS', 'SchradeISO', 'Scratch', 'SeXboX',
              'SecToR', 'SexFreaks', 'Shaver1912', 'SiBERiA', 'SiBV', 'SiC', 'SiGnuM', 'SiH', 'SiLENT', 'SiLENTGATE',
              'SiLVER', 'SiMPLEX', 'SiMPLiFY', 'SiN', 'SiNERGY', 'SiNGULARiTY', 'SiNiSTER', 'SiRE', 'SiRiON', 'SiSMiCV',
              'SiXAXis', 'SirVG', 'SkuLLs', 'SmokerZ', 'Smokerz', 'Sn0B', 'SnS', 'SoS', 'SofM', 'Souldrinker', 'SpT',
              'Squirrels', 'SrKmp3', 'Start2', 'Static', 'StyLe', 'SuPA', 'SuperX360', 'Supremacy', 'SweeTnDs', 'T3CH',
              'TALiON', 'TAM', 'TBE', 'TBS', 'TBT', 'TBTiSO', 'TC', 'TCA', 'TCD', 'TCG', 'TCGiSO', 'TCPA', 'TDD', 'TDJ',
              'TDK', 'TDMLiVE', 'TDT', 'TDU', 'TDUJAM', 'TE', 'TEAMISO', 'TEAMKNIGHTZ', 'TEAMKNiGHTZ', 'TEASPOON',
              'TECHBRiBE', 'TECHNiC', 'TED', 'TEDOX', 'TEMP', 'TEN', 'TERRA', 'TFG', 'TFTISO', 'TGX', 'THATSWHY',
              'THUNDER', 'THXiSO', 'THeBook', 'TIP', 'TJS', 'TM', 'TMD', 'TMFP', 'TNT', 'TR', 'TRDogs', 'TREASON',
              'TRIFORCE', 'TRM', 'TRN', 'TRPSpda', 'TRQ', 'TRSI', 'TRSi', 'TRVE', 'TRa', 'TRaSHMan', 'TS', 'TS4L',
              'TSAcISO', 'TSC', 'TUG', 'TURHCSKA', 'TV', 'TVC', 'TWCLIVE', 'TWCMP3', 'TWG', 'TWILIGHT', 'TWK',
              'TYPHOON', 'TZ7iSO', 'Tachyon', 'TcH', 'TeAsE', 'Thanks', 'TheAnalWhoreNextDoor', 'Thunder', 'TiMER',
              'TiNGO', 'TiNYiSO', 'TmN', 'TrT', 'TrueISO', 'TuF', 'Tyranny', 'UBD', 'UBE', 'UCC', 'UCF', 'UCS', 'UDP',
              'UKLiVE', 'UKP', 'UKT', 'UMC', 'UME', 'UMT', 'UNBAiSEDGOATS', 'UNIT', 'UNKNOWN', 'UNLiMiTED', 'UNS',
              'UNT', 'UNiQUE', 'UNiT', 'UPE', 'UPSIDE', 'US', 'USA', 'USELESS', 'USF', 'USR', 'USZ', 'UTB', 'UTE',
              'UTOPIA', 'UTZ', 'UVZ', 'Unknown', 'Unleashed', 'UpQ', 'Utopia', 'V4F', 'VACE', 'VAG', 'VAMPYRES',
              'VATOS', 'VDOX', 'VENGEANCE', 'VENOM', 'VF', 'VFi', 'VIGOR', 'VIMTO', 'VINYL', 'VL', 'VLiSO', 'VMA',
              'VMC', 'VNGCLONE', 'VOLCANO', 'VORTEX', 'VREX', 'VeRsAcE', 'ViC', 'ViGOR', 'ViLE', 'ViMTO', 'ViNTAGE',
              'ViRiLiTY', 'ViSTA', 'ViSiON', 'ViTALiTY', 'VinylMvZ', 'W.O.D', 'W.o.D', 'W00T', 'WAM', 'WAR3X', 'WARG',
              'WARIO', 'WAV', 'WDS', 'WEM', 'WHOA', 'WHORE', 'WHQRE', 'WIPICE', 'WL', 'WLM', 'WPR', 'WRE', 'WRG', 'WRM',
              'WTF', 'WTK', 'WUS', 'WW', 'WWR', 'WaLMaRT', 'WaYsTeD', 'WeeD', 'WerKLooS', 'WetNWild', 'WiC', 'WiCKED',
              'WiNE', 'WiSH4', 'WiZaRd', 'Wii', 'WiiCover', 'WiiD', 'WiiERD', 'WiiLP', 'WiiZARD', 'WiinSton', 'WjR',
              'WoD', 'WpR', 'WsR', 'Wurstsuppe', 'X360', 'XBLAminus', 'XBLAplus', 'XBOX', 'XBOX360', 'XBoX', 'XCESSiVE',
              'XCell', 'XD', 'XDOX', 'XDS', 'XDiViSiON', 'XEX', 'XMAS', 'XMM', 'XPA', 'XPG', 'XPM', 'XRB', 'XSR',
              'XSYTE', 'XSide', 'XTC', 'XTRiBE', 'XWaR', 'XXL', 'XXX', 'XaRT', 'Xdemo', 'XorCist', 'Xtas', 'Xtasy',
              'XtreaM', 'YARDVID', 'YLoD', 'YMiR', 'YPOGEiOS', 'YoshiKool', 'ZEKE', 'ZELDA', 'ZER0', 'ZHONGGUO',
              'ZOMBIES', 'ZONATiON', 'ZRL', 'ZRY', 'ZTX', 'ZZGiSO', 'ZiNE', 'Zio', 'Zonation', 'ZzZz', 'aAF', 'aSpYrE',
              'aSxDOX', 'aSxMV', 'aSxPDA', 'aSxPSx', 'alw', 'amrc', 'bC', 'bjm', 'c0w', 'cATiSO', 'cRacKPoTs',
              'caravan', 'cfb', 'chronic', 'cnmc', 'cps', 'cracker', 'dCZ', 'dKpZ', 'dM', 'dMp', 'darkforce',
              'deviance', 'dh', 'dnl', 'dumpTruck', 'eDG', 'eMF', 'eSpEcTrA', 'eXtaCY', 'eZ', 'emp', 'eurasia', 'f4a',
              'fedR', 'flt', 'frieNDS', 'gF', 'gTFiSO', 'ganGBAng', 'gayl0rd', 'gbatemp', 'gbt', 'gimpsRus', 'global',
              'gnvr', 'h00den', 'hM', 'hS', 'hV', 'hXc', 'hYdRoGeN', 'hYdroGeN', 'hbZ', 'i8', 'iCEmV', 'iCON', 'iFXP',
              'iGN', 'iHF', 'iHQ', 'iHX', 'iKu', 'iMARS', 'iMC', 'iMDz', 'iMF', 'iMMERSiON', 'iMPG', 'iMSDOX',
              'iMiTATiON', 'iNC', 'iNCiDENT', 'iND', 'iNDECLINE', 'iNDUCT', 'iNDeX', 'iNDiSO', 'iNFERi', 'iNLAWS',
              'iNSOMNi', 'iNSOMNiA', 'iNSOMNiES', 'iNSTANTPDA', 'iNSTEON', 'iNTENSiON', 'iNTERGANG', 'iNTGAMES',
              'iNVFX', 'iNViSiBLE', 'iONOS', 'iOSPDA', 'iPC', 'iPF', 'iPME', 'iPS', 'iPWNPDA', 'iR', 'iRGUN', 'iRO',
              'iRRM', 'iSO', 'iSOLATiON', 'iSOSPHERE', 'iSTP', 'iTRISO', 'iTWINS', 'iVEiSO', 'illuishorny', 'ind', 'jd',
              'jurai', 'k0tik', 'kW', 'kaMX', 'knk', 'ksi', 'kvz', 'mRu', 'mV4U', 'mVa', 'mVi', 'mbs', 'miracle',
              'miso', 'mkv', 'mvz', 'niRV', 'nuhs', 'oCN', 'omcx', 'ooze', 'orgasm', 'pMD', 'pND', 'pRAYparationH',
              'pSYCHOSiS', 'pSy360', 'pSyPSP', 'pXp', 'paranoid', 'patience', 'phEAR', 'plz', 'pmv', 'projectg', 'psed',
              'pyt', 'r18', 'rG', 'rGPDA', 'rH', 'rHViD', 'radial', 'rbk', 'rev', 'rpc', 'ryst', 'sUppLeX', 'sb', 'sfE',
              'smc', 'sour', 'srp', 'ss', 'tLOC', 'tRM', 'team', 'tjatburk', 'twee', 'uC', 'uF', 'uva', 'vme', 'vod',
              'w.o.d', 'w00t', 'wAx', 'wWs', 'wcs', 'weBITa', 'wpr', 'x0DuS', 'x360inT', 'xbox']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://indienova.com/gamedb',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache', }

release_type_dict = {
    'Full ISO': '1',
    'GGn Internal': '1',
    'P2P': '1',
    'Rip': '1',
    'Scrubbed': '1',
    'Home Rip': '1',
    'DRM Free': '1',
    'ROM': '1',
    'Other': '1',
    'Fix/Keygen': '3',
    'Update': '2',
    'DLC': '9',
    'GOG-Goodies': '5',
    'Trainer': '4',
    'Tool': '8',
    'Guide': '6',
    'Artwork': '5',
    'Audio': '7'
}

release_format_dict = {
    'Full ISO': '2',
    'GGn Internal': '4',
    'P2P': '4',
    'Rip': '3',
    'Scrubbed': '7',
    'Home Rip': '4',
    'DRM Free': '5',
    'ROM': '1',
}

platform_dict = {'Switch': '20', 'Game Boy Advance': '24', 'Game Boy': '22', 'Game Boy Color': '22', 'Wii U': '30',
                 'Wii': '30',
                 'Mac': '37', 'iOS': '38',
                 'Windows': '16', 'DOS': '17', 'Xbox': '18', 'Xbox 360': '19',
                 'PlayStation 1': '32', 'PlayStation 2': '33', 'PlayStation 3': '35', 'PlayStation 4': '31',
                 'PlayStation Vita': '36', 'PlayStation Portable': '34',
                 'Android': '45',
                 'Linux': '46'}


def true_input(content):
    while True:
        output = input(content)
        if output == '':
            print('输入内容不能为空！')
        else:
            return output


def find_indie(game_name):
    api_url = 'https://indienova.com/get/gameDBName'
    num = 1
    params = {'query': game_name}
    data = {}
    res = requests.get(api_url, headers=headers, params=params).json()
    for i in res:
        data[str(num)] = i
        num += 1
    return data


class GGnApi:
    def __init__(self, dl_link, cookies=None):
        self.session = requests.Session()
        self.session_cookies = cookies
        self.session.headers = headers
        self.dl_link = dl_link
        self.torrent_id = re.search(r'id=(\d+)', dl_link).group(1)

    def _install_cookies(self):
        if not self.session_cookies:
            with open('cookies.json', 'r') as r:
                cookies = json.load(r)
            cookies = scatfunc.cookie2dict(cookies['ggn'])
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        else:
            return None

    def _find_store(self):
        url = 'https://gazellegames.net/torrents.php?torrentid={}'.format(self.torrent_id)
        url = self.session.get(url).url
        res = self.session.get(url)
        self.res_soup = BeautifulSoup(res.text, 'lxml')
        self.name = re.search(r'-\s(.+)\s\(\d{4}', self.res_soup.select_one('#display_name').text).group(1)
        try:
            self.steam = self.res_soup.select_one('a[href^="https://store.steampowered.com/app/"][title="Steam"]')[
                'href']
        except TypeError:
            self.steam = None
        try:
            self.epic = self.res_soup.select_one('a[href^="https://www.epicgames.com/store"][title="EpicGames"]')[
                'href']
        except TypeError:
            self.epic = None
        return {'steam': self.steam, 'epic': self.epic}

    def _copy_desc(self):
        url = 'https://gazellegames.net/torrents.php?action=edit&id={}'.format(self.torrent_id)
        # url = 'http://127.0.0.1:85/ggn5.html'
        desc = self.session.get(url)
        desc_soup = BeautifulSoup(desc.text, 'lxml')
        self.torrent_desc = desc_soup.select_one('#release_desc').text.replace('[align=center]', '').replace('[/align]',
                                                                                                             '')
        self.release_title = desc_soup.select_one('#release_title').get('value').replace('/', '')
        if desc_soup.select_one('#remaster_title'):
            self.release_title += '-GOG' if 'GOG' in desc_soup.select_one('#remaster_title').get(
                'value').upper() else ''
        self.release_type = desc_soup.select_one('#miscellaneous option[selected="selected"]').text
        if self.release_type == 'GameDOX':
            self.release_type = desc_soup.select_one('#gamedox option[selected="selected"]').text
        self.scene = 'yes' if self.release_type.split('-')[-1] in scene_list else 'no'
        self.verified = 'yes' if self.release_type in 'P2P DRM Free' else 'no'
        self.platform = desc_soup.select_one('#platform option[selected="selected"]').text
        return self.torrent_desc

    def _download_torrent(self):
        res = self.session.get(self.dl_link)
        torrent = bytes()
        for chunk in res.iter_content(100000):
            torrent += chunk
        ggn_dir = os.path.join(torrent_dir, 'ggn/')
        if not os.path.exists(ggn_dir):
            os.makedirs(ggn_dir)
        with open(os.path.join(ggn_dir, os.path.basename('[GGn]{}.torrent'.format(self.release_title))),
                  'wb') as t:
            t.write(torrent)
        torrent = bencodepy.decode(torrent)
        torrent[b'announce'] = b'https://tracker.pterclub.com/announce?passkey=' + bytes(pter_key, encoding='utf-8')
        torrent[b'info'][b'source'] = bytes('[pterclub.com] ＰＴ之友俱乐部', encoding='utf-8')
        del torrent[b'comment']
        torrent = bencodepy.encode(torrent)
        with open(os.path.join('torrents', os.path.basename('[PTer]{}.torrent'.format(self.release_title))), 'wb') as t:
            t.write(torrent)

    def _return_terms(self):
        attr = {}
        for name, value in vars(self).items():
            attr[name] = value
        del attr['res_soup']
        del attr['session']
        return attr

    def worker(self):
        self._install_cookies()
        print('正在获取游戏信息...')
        self._find_store()
        print('正在获取种子信息...')
        self._copy_desc()
        print('正在下载种子...')
        self._download_torrent()
        return self._return_terms()


class PTerApi:
    def __init__(self, ggn_info, cookies=None):
        self.session = requests.Session()
        self.session_cookies = cookies
        self.session.headers = headers
        self.name = ggn_info['name']
        self.platform = ggn_info['platform']
        self.steam = ggn_info['steam']
        self.epic = ggn_info['epic']
        self.release_title = ggn_info['release_title']
        self.release_type = ggn_info['release_type']
        self.torrent_desc = ggn_info['torrent_desc']
        self.scene = ggn_info['scene']
        self.verified = ggn_info['verified']
        self.gid = None

    def _install_cookies(self):
        if not self.session_cookies:
            with open('cookies.json', 'r') as r:
                cookies = json.load(r)
            cookies = scatfunc.cookie2dict(cookies['pter'])
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        else:
            return None

    def _find_game(self):
        url = 'https://pterclub.com/searchgameinfo.php'
        data = {'name': self.name}
        # data = {'name':'into'}
        res = self.session.post(url, data=data)
        res_soup = BeautifulSoup(res.text, 'lxml')
        user_class = res_soup.select_one('a[href^="userdetails.php?id="][class$="_Name"]')['class'][0].split('_')[0]
        uplev = 'ModeratorAdministratorUploaderSysOp'
        if user_class in uplev:
            self.uplver = 'yes'
        else:
            self.uplver = 'no'
        game_list = res_soup.select('a[title="点击发布这游戏设备的种子"]')
        platform_list = res_soup.select('img[src^="/pic/category/chd/scenetorrents/"]')
        if not game_list:
            return None
        game_dict = {}
        num = 1
        for game, platform in zip(game_list[::2], platform_list):
            gid = re.search(r'detailsgameinfo.php\?id=(\d+)', game['href']).group(1)
            game_dict[str(num)] = '{}: {} GID:{}'.format(platform['title'], game.text, gid)
            num += 1
        print('将要上传的种子是：{}\n我们在猫站找到以下游戏，请选择要上传的游戏分组（输入编号(并非gid)即可，如果没有请输入0）：').format(self.release_title)
        for num, game in game_dict.items():
            print('{}.{}'.format(num, game))
        gid = (true_input('编号： '))
        if gid == '0':
            return None
        print(game_dict[gid])
        gid = re.search(r'GID:(.+)', game_dict[gid]).group(1)
        print(gid)
        self.gid = gid
        return gid

    def _upload_game(self):
        url = 'https://pterclub.com/takeuploadgameinfo.php'
        if self.steam:
            game_info = scatfunc.steam_api(self.steam)
        elif self.epic:
            game_info = scatfunc.epic_api(self.epic)
        else:
            print('未找到steam或epic链接，正在前往indenova查询\n... ... ...')
            indie_data = find_indie(self.name)
            for i in indie_data:
                print('{}.{}'.format(i, re.sub('http.+', '', indie_data[i]['title'])))
            indie_data = indie_data[input('请输入适配游戏的序号,没有请直接回车：')]['slug']
            if indie_data == '':
                return False
            game_info = scatfunc.indie_nova_aip(indie_data)

        data = {'uplver': self.uplver, 'detailsgameinfoid': '0', 'name': self.name, 'color': '0', 'font': '0',
                'size': '0', 'descr': game_info['about'], 'console': platform_dict[self.platform],
                'year': game_info['year'],
                'has_allowed_offer': '0',
                'small_descr': game_info['chinese_name'] if 'chinese_name' in game_info else input('请输入游戏中文名')}
        game_url = self.session.post(url, data=data).url
        gid = re.search(r'detailsgameinfo.php\?id=(\d+)', game_url).group(1)
        self.gid = gid

    def _upload_torrent(self):
        url = 'https://pterclub.com/takeuploadgame.php'
        torrent_file = os.path.join(torrent_dir, '[PTer]{}.torrent'.format(self.release_title))
        file = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
        data = {'uplver': self.uplver, 'categories': release_type_dict[self.release_type],
                'format': release_format_dict[self.release_type] if self.release_type in release_format_dict else '7',
                'has_allowed_offer': '0', 'gid': self.gid,
                'descr': self.torrent_desc}
        region = true_input('请选择种子地区（直接输入数字即可）：\n1.大陆\n2.香港\n3.台湾\n4.英美\n5.韩国\n6.日本\n7.其它\n')
        if self.scene == 'yes':
            data['sce'] = self.scene
        if self.verified == 'yes':
            data['vs'] = self.verified
        if input('该资源是否有中文？（yes/no）默认为no：') == 'yes':
            data['zhongzi'] = 'yes'
        if input('该资源是否有国语？(yes/no) 默认为no：') == 'yes':
            data['guoyu'] = 'yes'
        data['team'] = region
        short_name = scatfunc.back0day(self.name, self.release_title)
        print(self.release_title)
        user_title = input('智能检测到的种子标题为{}，若有错误，请输入正确的标题，没有请直接回车：'.format(short_name))
        user_title = short_name if user_title == '' else user_title
        data['name'] = user_title
        print('正在上传... ...')
        self.session.post(url, data=data, files=file)

    def worker(self):
        self._install_cookies()
        print('正在搜索猫站游戏列表...')
        self._find_game()
        if self.gid is None:
            print('未找到相关游戏，正在上传游戏资料...')
            if self._upload_game() is False:
                return 0
        print('正在上传种子...')
        self._upload_torrent()


if __name__ == '__main__':
    find_indie('刺客信条')
    # ggn = GGnApi('none')
    # ggn._download_torrent()
