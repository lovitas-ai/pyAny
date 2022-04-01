
from datetime import datetime
import pandas as pd

print("Starte das Programm")

bev_org=pd.read_excel(r'C:\Users\lovit\Desktop\DEV\Dashboard_Bev\Konzept\Bev_data.xlsx',dtype={'AGS': int, 'Kreis': str,'Jahr': datetime,'Geschlecht': str,'Altersjahre': str,'Bevoelkerung': int})
print("Einlesen erfolgreich")

bev_org["J"]=pd.DatetimeIndex(bev_org['Jahr']).year
bev_org["A"]=bev_org['Altersjahre'].str[:2]
bev_org['A'] = bev_org['A'].str.replace('un','0')
bev_org['A'] = bev_org['A'].astype(int)

geschlecht=bev_org.groupby(['Geschlecht','J','A','Altersjahre','Kreis'])[['Bevoelkerung']].agg('sum').reset_index()

p_g_a_20=geschlecht.pivot(index=['A','Altersjahre','J','Kreis'], columns=['Geschlecht'], values='Bevoelkerung').reset_index()

df_01=p_g_a_20
print(df_01.head(10))


