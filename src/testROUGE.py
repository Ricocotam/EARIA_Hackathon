import rouge
import nltk

apply_avg = 'Avg'
apply_best = 'Best'

evaluator = rouge.Rouge(metrics=['rouge-n'],
                       max_n=3,
                       limit_length=True,
                       length_limit=100,
                       length_limit_type='words',
                       apply_avg=apply_avg,
                       apply_best=apply_best,
                       alpha=0.5, # Default F1_score
                       weight_factor=1.2,
                       stemming=True)


hypothesis_1 = "King Norodom Sihanouk has declined requests to chair a summit of Cambodia 's top political leaders , saying the meeting would not bring any progress in deadlocked negotiations to form a government .\nGovernment and opposition parties have asked King Norodom Sihanouk to host a summit meeting after a series of post-election negotiations between the two opposition groups and Hun Sen 's party to form a new government failed .\nHun Sen 's ruling party narrowly won a majority in elections in July , but the opposition _ claiming widespread intimidation and fraud _ has denied Hun Sen the two-thirds vote in parliament required to approve the next government .\n"
references_1 = ["Prospects were dim for resolution of the political crisis in Cambodia in October 1998.\nPrime Minister Hun Sen insisted that talks take place in Cambodia while opposition leaders Ranariddh and Sam Rainsy, fearing arrest at home, wanted them abroad.\nKing Sihanouk declined to chair talks in either place.\nA U.S. House resolution criticized Hun Sen's regime while the opposition tried to cut off his access to loans.\nBut in November the King announced a coalition government with Hun Sen heading the executive and Ranariddh leading the parliament.\nLeft out, Sam Rainsy sought the King's assurance of Hun Sen's promise of safety and freedom for all politicians.",
                "Cambodian prime minister Hun Sen rejects demands of 2 opposition parties for talks in Beijing after failing to win a 2/3 majority in recent elections.\nSihanouk refuses to host talks in Beijing.\nOpposition parties ask the Asian Development Bank to stop loans to Hun Sen's government.\nCCP defends Hun Sen to the US Senate.\nFUNCINPEC refuses to share the presidency.\nHun Sen and Ranariddh eventually form a coalition at summit convened by Sihanouk.\nHun Sen remains prime minister, Ranariddh is president of the national assembly, and a new senate will be formed.\nOpposition leader Rainsy left out.\nHe seeks strong assurance of safety should he return to Cambodia.\n",
                ]

scores = evaluator.get_scores(hypothesis_1, references_1)
print(scores['rouge-1']['f'])
print(scores['rouge-2']['f'])
print(scores['rouge-3']['f'])

