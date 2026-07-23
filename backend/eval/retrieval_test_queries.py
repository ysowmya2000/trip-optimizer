"""
Manually labeled retrieval test queries for the RAG retrieval eval.

correct_ids were labeled by inspecting the actual ChromaDB collection
(travel_knowledge) for each (destination, category) pair - every document
seeded under that destination+category tag during app/db/seed_attractions.py
is treated as a genuinely correct result for the query, since seeding used
real Google Places category searches (e.g. "temples in Bangkok" really
returned temple-tagged results - spot-checked manually during Phase 0).
This is the one-time manual labeling step; these ids are not derived from
running semantic search itself, so scoring against them is not circular.
"""

RETRIEVAL_TEST_QUERIES = [
    {
        "query": 'temples in Bangkok',
        "destination": 'Bangkok',
        "category": 'temples',
        "correct_ids": ['attr_ChIJ5Wl37g6Z4jARiP4itarBPDQ', 'attr_ChIJaSv_6gaZ4jARnbiUVn6Z_YY', 'attr_ChIJP-MtN12Z4jARlEBmga-oF4w', 'attr_ChIJvccM01iZ4jARPwr8_uBuM_8', 'attr_ChIJg-IqNBGZ4jAR0dPx_MR-gTk', 'attr_ChIJ4VPDiQKZ4jARdfHoseVonFk', 'attr_ChIJ_bd56myZ4jAROGViXBy9vP0', 'attr_ChIJA7PG9AuZ4jARIyvh-TR_wkA', 'attr_ChIJvwXXwEWY4jARC2dj117syBA', 'attr_ChIJa4tZORCZ4jARdCUEjuI59eo'],
    },
    {
        "query": 'street food in Bangkok',
        "destination": 'Bangkok',
        "category": 'food',
        "correct_ids": ['attr_ChIJLWlCk9GY4jARpNGpRcq5ABY', 'attr_ChIJC2PZegCZ4jAR7tyqaMPS38s', 'attr_ChIJje_pHwCZ4jAR52gik_-LBT0', 'attr_ChIJj4-sPwCZ4jARhq4jmNOn1Yw', 'attr_ChIJYXEMGACZ4jAR6-ByPaeWtr8', 'attr_ChIJhzewhWqZ4jARkjTpeifVZk8', 'attr_ChIJU0gJz1iZ4jARB3hEbe2cwGE', 'attr_ChIJp5jKGQCZ4jAR4l0DCdvPrLo', 'attr_ChIJm9eXpcuZ4jAROxvGhh77SsY', 'attr_ChIJ89uLVgCf4jAR5AAlCha57tQ'],
    },
    {
        "query": 'nightlife in Bangkok',
        "destination": 'Bangkok',
        "category": 'nightlife',
        "correct_ids": ['attr_ChIJI1joEm2Z4jAR1RIdaTWebBQ', 'attr_ChIJVTBnbMWY4jARzZ5CS7DwHVk', 'attr_ChIJR4LgSl-f4jARSMzR8x4RA3E', 'attr_ChIJ5178Viqf4jARZKFL40SO2RU', 'attr_ChIJ0Sf6Yiyf4jARebisewq7E-4', 'attr_ChIJBT9pW_aZ4jARnygIc5iuupE', 'attr_ChIJF4OXv_WZ4jARbcNPlcou0Yo', 'attr_ChIJ6fTp2buf4jARfkwPiyFfOKs', 'attr_ChIJaWYJu8-e4jARCqFsNRnGKxo', 'attr_ChIJF0QAycSY4jARv3t4vwi1r8A'],
    },
    {
        "query": 'street food in Hanoi',
        "destination": 'Hanoi',
        "category": 'food',
        "correct_ids": ['attr_ChIJf_4Ie7-rNTERqD8UU8HVyhA', 'attr_ChIJOWzaPxGrNTERlksVQI3wIzI', 'attr_ChIJtRY3u3SrNTERs95UQ9jA--s', 'attr_ChIJUZwaffmrNTER3zljQzqBUOY', 'attr_ChIJY89m6cCrNTERG-N0Fy4dWBw', 'attr_ChIJJci6wKyrNTER59o2N4mdFY4', 'attr_ChIJ_4KkypOrNTERConxQCyztMs', 'attr_ChIJi2-Icb-rNTEROu-_GUt4eQk', 'attr_ChIJrSnreyyrNTERerYhe3EwyaA', 'attr_ChIJBc_8ksCrNTER7xjIdzUga9w'],
    },
    {
        "query": 'temples in Hanoi',
        "destination": 'Hanoi',
        "category": 'temples',
        "correct_ids": ['attr_ChIJr7enHa-rNTERbivpCTqoenY', 'attr_ChIJp56AAMCrNTERHTeCAuwWJ7s', 'attr_ChIJZ73nJpmrNTERHt_VdIgHDlg', 'attr_ChIJ9Y3KR7-rNTERawQ7FeFv5gA', 'attr_ChIJwyFZi6WrNTER76sqY7OcMjE', 'attr_ChIJ7XWEcqGrNTERrsLf6W8259s', 'attr_ChIJz0aH0VyrNTERrhRrKTcIFxk', 'attr_ChIJMciE-GmrNTERfjkshGzwPNE', 'attr_ChIJ_WxOh-aqNTERU3pju0DhjDE', 'attr_ChIJuerTwf2qNTERnvjmhZRDyik'],
    },
    {
        "query": 'nature parks in Prague',
        "destination": 'Prague',
        "category": 'nature',
        "correct_ids": ['attr_ChIJG4u6e9GVC0cRdd_jlTayJzU', 'attr_ChIJbSZndNuUC0cR2lgM9o_zW5Q', 'attr_ChIJ2QFPvc-UC0cR-yep7ub8N78', 'attr_ChIJ3UB98gKVC0cRwGV3D_tmxY4', 'attr_ChIJ936RN22VC0cR5aIolrcYls4', 'attr_ChIJEw1qJX6UC0cRZz0wkkTsrcg', 'attr_ChIJ4eTG7OSUC0cRXMru0PQo-Kk', 'attr_ChIJ0alOyKOVC0cRkAZcOn8ZvjI', 'attr_ChIJJ-XP9uCUC0cRXB0IHy2hMtU', 'attr_ChIJ-53TmZqUC0cRiqnBgT93RXQ'],
    },
    {
        "query": 'nightlife in Prague',
        "destination": 'Prague',
        "category": 'nightlife',
        "correct_ids": ['attr_ChIJm3K2Pe2UC0cRr_kkQrOB3D8', 'attr_ChIJV3BqjuWUC0cRYMoGwBtnyz4', 'attr_ChIJfWDMYuqUC0cRb7F2dVLFPQI', 'attr_ChIJexiRhu-UC0cRB-QVJcw_FR0', 'attr_ChIJ4b6ugO6UC0cRKmnm1vbtoLc', 'attr_ChIJ9V2L5iyVC0cRkELIMIDHCwI', 'attr_ChIJcUpsX--UC0cRNOGndauddng', 'attr_ChIJTRGoFbWUC0cRczZMAqrg0X8', 'attr_ChIJh0E5jumUC0cR7bhXrpqrBl4', 'attr_ChIJaeDSJe2UC0cRFIC2qKGlfEI'],
    },
    {
        "query": 'nightlife in Paris',
        "destination": 'Paris',
        "category": 'nightlife',
        "correct_ids": ['attr_ChIJVYQc4ehv5kcRxAmY5t4c54k', 'attr_ChIJq-XFUR9u5kcRgSahYxl9IhE', 'attr_ChIJE3H94B5u5kcRNtRSYm7Myfw', 'attr_ChIJM0zuNexv5kcRRO9O90zTvoA', 'attr_ChIJiegK5OBx5kcR9t1Ycr1Bz1g', 'attr_ChIJJUvyzgBy5kcRtvSiuA5hvpE', 'attr_ChIJp7wGa-xv5kcRHl_5cQQA_Ek', 'attr_ChIJ-xK88-1z5kcRHWabGDpij6Y', 'attr_ChIJw-i9w35v5kcR-EuieLb04jg', 'attr_ChIJ88rPsBlu5kcREsV3u2lhALM'],
    },
    {
        "query": 'museums in Paris',
        "destination": 'Paris',
        "category": 'museums',
        "correct_ids": ['seed_5', 'attr_ChIJD3uTd9hx5kcR1IQvGfr8dbk', 'attr_ChIJG5Qwtitu5kcR2CNEsYy9cdA', 'attr_ChIJo6qq6i5u5kcRCpYBp4rQP9w', 'attr_ChIJQ9vMHipw5kcRWHC2ESjYaGQ', 'attr_ChIJfRtS-QBu5kcRwRg5JXVrwcg', 'attr_ChIJS2t0QgFu5kcR92388prakcE', 'attr_ChIJY8922uBv5kcRJESw9l2dlLc', 'attr_ChIJSUOPztFv5kcRnEbSPYG-9fM', 'attr_ChIJpfWut8dv5kcRLTqTTLiFd10', 'attr_ChIJLxPh9d1x5kcRf7M1U0pu1gU'],
    },
    {
        "query": 'museums in Rome',
        "destination": 'Rome',
        "category": 'museums',
        "correct_ids": ['attr_ChIJq-bXVgRhLxMRv3vgOXaktBs', 'attr_ChIJ8-wGeU9gLxMR--zJtnpGod4', 'attr_ChIJKcGbg2NgLxMRthZkUqDs4M8', 'attr_ChIJPRgYblBgLxMRB--q_Tzt4wY', 'attr_ChIJF0obe01gLxMR0JJHtlD0kMY', 'attr_ChIJxcyMIv1gLxMRKAH_Dv2q8iw', 'attr_ChIJjT_cwulgLxMRbL2aAaLagKw', 'attr_ChIJ18PTgaZhLxMRvINaLw9AZ2w', 'attr_ChIJlSkdkeRgLxMREkRxyk8IJEY', 'attr_ChIJbedagU9gLxMRdw-SiQm53EM'],
    },
    {
        "query": 'parks in Rome',
        "destination": 'Rome',
        "category": 'nature',
        "correct_ids": ['attr_ChIJj1M8HQJhLxMRRI6D_z18Pes', 'attr_ChIJ2dxWXTRgLxMR-Ug5hzOYuQM', 'attr_ChIJYeUz0BpgLxMRBNr_z8ge-CA', 'attr_ChIJa-FrY0BgLxMRDN1UR07SMIE', 'attr_ChIJ-Z2cHUBgLxMRz8Wfw_RW_Qw', 'attr_ChIJCajXkAiKJRMREV4n39850EU', 'attr_ChIJr6NTMQNhLxMRLLrdJ-dMGOg', 'attr_ChIJBeoiURqKJRMRCVOXmu4EKqo', 'attr_ChIJOwPcv0FgLxMRALWOCzn7gbU', 'attr_ChIJ46sD-LlhLxMR0TuCx56rFYc'],
    },
    {
        "query": 'markets in Mumbai',
        "destination": 'Mumbai',
        "category": 'markets',
        "correct_ids": ['attr_ChIJn079zr_R5zsR3Ghy0UQ2dCM', 'attr_ChIJI1VscN7R5zsRO3y8QF7i6PY', 'attr_ChIJRcmQYUHP5zsRu8k34sDz00w', 'attr_ChIJ__-jRTvO5zsR6iycCnFj2_Y', 'attr_ChIJZ6fUhLjP5zsRHNZ5poAWy88', 'attr_ChIJr6Jh-R7P5zsRZWFXrjNFc-4', 'attr_ChIJCWkEg5bR5zsRpPydldURcBk', 'attr_ChIJJf1rhybO5zsRpArb-NaAh5o', 'attr_ChIJAQbWki_O5zsRLKU6gF0-vUo', 'attr_ChIJLxXB-UnO5zsRJVW-TlnDoyM'],
    },
    {
        "query": 'street food in Mumbai',
        "destination": 'Mumbai',
        "category": 'food',
        "correct_ids": ['attr_ChIJOW5d0SLR5zsRdOb864OWRxg', 'attr_ChIJL0EwAI_O5zsRKTWGclEoGgA', 'attr_ChIJ_____9rR5zsRVLmjr1z4zTY', 'attr_ChIJ0Wg9FOjR5zsRGkTJnja8CyA', 'attr_ChIJsYFP93jR5zsRcKWa8kY7-Ig', 'attr_ChIJiX_ZAZfP5zsRuJxP0HW1tZo', 'attr_ChIJOZdnQwfR5zsRBarhOYp355c', 'attr_ChIJK7D_sczR5zsRph3XOWbNdfA', 'attr_ChIJwWOPJdnR5zsRcgxEPKsyPsI', 'attr_ChIJ4SJfxNvR5zsRP8iG8rtu0O8'],
    },
    {
        "query": 'architecture in Barcelona',
        "destination": 'Barcelona',
        "category": 'architecture',
        "correct_ids": ['seed_6', 'attr_ChIJ1eGKmZOipBIRah43T2Kjn8Q', 'attr_ChIJYUFLSe2ipBIRD04uni940kA', 'attr_ChIJQQSrd_qipBIRQ2xzarVkqn8', 'attr_ChIJO5k2-JOipBIRxfDsj5VkasE', 'attr_ChIJoXZqNuOipBIRsZU39a8r_qk', 'attr_ChIJHQufE_mipBIRXhKyv6uiJNY', 'attr_ChIJJ0AB4M-ipBIRj3HSiyLF-gE', 'attr_ChIJq0HUUq6ipBIRWM6qGqALmok', 'attr_ChIJ160fSTajpBIRZlKRfkwTn1U', 'attr_ChIJJ2JbaneipBIRpVQ6RTJSwLA'],
    },
    {
        "query": 'local food in Barcelona',
        "destination": 'Barcelona',
        "category": 'food',
        "correct_ids": ['seed_7', 'attr_ChIJfzr5EfWipBIRbpBQmkaOrNI', 'attr_ChIJef1HPBWjpBIRnbC1J-cB5W8', 'attr_ChIJA-c18FeipBIRw8n-UGwjVLk', 'attr_ChIJf8Zst1-jpBIRkov6YZvFOpY', 'attr_ChIJk4PX9FWipBIR4BejEaOwXzw', 'attr_ChIJz7Jj3beipBIReQW92-l4bWk', 'attr_ChIJFxjdR4ujpBIRS6tPThMEn1w', 'attr_ChIJ1-Cye6OipBIRxpfgjCDejPk', 'attr_ChIJA_gqnRu9pBIRNpT3-5KeMZc', 'attr_ChIJSwkRFKGjpBIRvuaV6WtgXg4'],
    },
    {
        "query": 'shopping in Tokyo',
        "destination": 'Tokyo',
        "category": 'shopping',
        "correct_ids": ['attr_ChIJscDhJ4SLGGARbx0GlzPi9ng', 'attr_ChIJP6jlUFiLGGAR5fwuswd1KXA', 'attr_ChIJcyH-4qiMGGARGzk4lZCx2xo', 'attr_ChIJ_TibA9qMGGARNYmVIFyGU9k', 'attr_ChIJhxxszamMGGARcuAXpFunolU', 'attr_ChIJ7WUBoDGLGGARaK3ikXtAfDg', 'attr_ChIJ05576NmMGGARlCnERJue3Y4', 'attr_ChIJr4J6pKmMGGARdQLOgrzToH4', 'attr_ChIJj0CdfaSMGGAROHhLfxE208o', 'attr_ChIJ_9GsagCNGGAR6auqGPod5nY'],
    },
    {
        "query": 'rooftop bars in Dubai',
        "destination": 'Dubai',
        "category": 'nightlife',
        "correct_ids": ['attr_ChIJf2jFdoxCXz4RN9goPAKvuN8', 'attr_ChIJtcrHqmRDXz4R5LhkoE7ibHU', 'attr_ChIJLXpp_bdDXz4RdPUPqcJ4nN4', 'attr_ChIJ2wkf03ZDXz4RBbs1HOWlS1M', 'attr_ChIJWYnl2GVCXz4RJBRxguVWjNI', 'attr_ChIJaQeMqdVpXz4Rc8XQJD-u4Sc', 'attr_ChIJI8kQb4JpXz4RQ-d688uTPgk', 'attr_ChIJh2RqzN1DXz4RBXw--Qi_xCY', 'attr_ChIJE0s1XJtDXz4RIMkKjK0EGMQ', 'attr_ChIJAd5eP65DXz4R59kt0aT4Vqs'],
    },
    {
        "query": 'historical sites in Dubai',
        "destination": 'Dubai',
        "category": 'historical',
        "correct_ids": ['attr_ChIJ____cw5CXz4RN2I0Y4Iwexs', 'attr_ChIJV_ZX__1pXz4RrY7C46fQmqI', 'attr_ChIJQZ3ZINtCXz4RmFeoAa81MPk', 'attr_ChIJWQnUnqVCXz4RuFhIAP-PUGE', 'attr_ChIJS-JnijRDXz4R4rfO4QLlRf8', 'attr_ChIJg9RcIqJdXz4RApPMGPfQvCQ'],
    },
    {
        "query": 'viewpoints in Lisbon',
        "destination": 'Lisbon',
        "category": 'nature',
        "correct_ids": ['attr_ChIJV32DNI8zGQ0R9GqiWeuNH2E', 'attr_ChIJx-Rwl4QzGQ0RaSfN7SE7IEE', 'attr_ChIJYzmNq4kzGQ0R8PmcMe8PyEY', 'attr_ChIJYQgAN4AzGQ0RoeNtM3J56xs', 'attr_ChIJlwybZnY0GQ0RwvOJskKjhrs', 'attr_ChIJQzXGs5EzGQ0RAytgn6leEcM', 'attr_ChIJ9x5tKAA1GQ0RgCwYXAaOkQI', 'attr_ChIJH1dSp9tSzpQROFvFiXlCrdw', 'attr_ChIJeXctVnIzGQ0RNfNVqdSTjO4', 'attr_ChIJLZJmepk0GQ0RIHStkdNe7cI'],
    },
    {
        "query": 'food in Lisbon',
        "destination": 'Lisbon',
        "category": 'food',
        "correct_ids": ['attr_ChIJkZDZjXY0GQ0R-4fI-zFNv0I', 'attr_ChIJfdVbOHc0GQ0Rf-x1kKZ2QAE', 'attr_ChIJvYRI69EzGQ0RCOyhk1c0hLQ', 'attr_ChIJqQFcEHo0GQ0RvCnL-bpescs', 'attr_ChIJgVZPx641GQ0RNvMNthOjyF4', 'attr_ChIJtx4y4YkzGQ0RJADhVgp16xc', 'attr_ChIJdWBeWYc0GQ0RktxySU7hjxM', 'attr_ChIJQ68wysA1GQ0Ruvjt8Qn31MM', 'attr_ChIJ_-dU9g8zGQ0RZuM8v0sKEt8', 'attr_ChIJbQ3MO1czGQ0RvXZ7l0nWbVk'],
    },
]
