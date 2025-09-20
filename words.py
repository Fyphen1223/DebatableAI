import parlant.sdk as p

async def add_domain_glossary(agent: p.Agent) -> None:
  await agent.create_term(
    name="ディベート",
    description="ある一つの論題（プラン、Pとも）に関して、肯定側と否定側に分かれて議論を行う競技。",
  )

  await agent.create_term(
	name="試合の流れ",
	description="一立制の場合、肯定側立論、否定側質疑、否定側立論、肯定側質疑、否定側第一反駁、肯定側第一反駁、否定側第二反駁、肯定側第二反駁の順に行われる。二立制の場合、肯定側第一立論、否定側第一質疑、否定側第一立論、肯定側第一質疑、肯定側第二立論、否定側第二質疑、否定側第二立論、肯定側第二質疑、否定側第一反駁、肯定側第一反駁、否定側第二反駁、肯定側第二反駁の順に行われる。",
  )

  await agent.create_term(
	name="アタック",
	description="ディベートにおいて、相手の主張に対して反論をすること。",
  )

  await agent.create_term(
	name="ブロック",
	synonyms=["防御", "再反駁", "再反"],
	description="ディベートにおいて、相手の反駁に対して反駁すること。",
  )
  
  await agent.create_term(
	name="立つ",
	description="ディベートにおいて、議論が成立していることを指す言葉。",
  )

  await agent.create_term(
	name="切れている",
	description="ディベートにおいて、議論が成立していないことを指す言葉。",
  )

  await agent.create_term(
	name="ドロップ",
	synonyms=["落ちる"],
	description="ディベートにおいて、相手の主張に対して反論や質問をせずに放置すること。これにより、その主張が自動的に受け入れられ、議論が不利になる可能性がある。",
  )
  
  await agent.create_term(
	name="レート",
	synonyms=["レイト"],
	description="ディベートの一部の状況において、ドロップされている議論に触れてしまうこと。反則。",
  )

  await agent.create_term(
    name="プラン",
    synonyms=["P"],
    description="ディベートにおいて、肯定側が提案する解決策や政策の事。Pと略されることもある。",
  )

  await agent.create_term(
    name="肯定側",
    synonyms=["Aff", "肯定", "アファ"],
    description="ディベートにおいて、論題を支持する立場のこと。",
  )

  await agent.create_term(
    name="否定側",
    synonyms=["Neg", "否定", "ネガ"],
    description="ディベートにおいて、論題に反対する立場のこと。",
  )

  await agent.create_term(
    name="フロー",
    description="ディベートにおいて、議論の流れや展開を記録するためのノートや図表のこと。",
  )

  await agent.create_term(
    name="トピカリティ",
    description="議論の焦点となるテーマや問題の重要性を示す概念。これに反すると、議論が無関係または不適切と見なされ、負けとなる可能性がある。",
  )
  
  await agent.create_term(
    name="メリット",
	synonyms=["AD", "M"],
    description="なぜプランを導入することが良いことなのかという事を説明するための根拠や理由。肯定側の立論で出される。",
  )
  
  await agent.create_term(
    name="デメリット",
	synonyms=["DA", "DM"],
    description="なぜプランを導入することが良いことではないのかという事を説明するための根拠や理由。否定側の立論で出される。",
  )
  
  await agent.create_term(
    name="一立制",
    description="立論を肯定側、否定側ともに一回ずつ行う形式。基本は反駁は含まれない。高校生ディベート甲子園などで採用されている。比較的簡単な形式。",
  )

  await agent.create_term(
    name="二立制",
    synonyms=["二立", "2con"],
    description="立論を肯定側、否定側ともに二回ずつ行う形式。この立論には反駁も含まれる。JDA等で採用されている。比較的複雑な形式。",
  )

  await agent.create_term(
    name="立論",
    description="ディベートにおいて、肯定側または否定側が自分たちの主張や意見を述べること。肯定側はプランのメリットを、否定側はデメリットを述べる。",
  )
  
  await agent.create_term(
	name="三要素",
	description="肯定側では、内因性、解決性、重要性の3点。否定側では、固有性、発生過程、深刻性の3点。これらのどれかが欠けていたり、反駁されると負けとなる可能性がある。",
  )

  await agent.create_term(
	name="内因性",
	synonyms=["Inh", "N"],
	description="プランがどのような問題を解決するのかという立証をする部分。複数ある場合は、Inh1, Inh2, 等と表記することもある。",
  )

  await agent.create_term(
	name="解決性",
	synonyms=["Sol", "ソルベンシー", "K"],
	description="プランがなぜ内因性で述べた問題を解決できるのかという立証をする部分。複数ある場合は、Sol1, Sol2, 等と表記することもある。",
  )

  await agent.create_term(
	name="重要性",
	synonyms=["Sig", "インパクト", "J"],
	description="プランが議論の焦点となるテーマや問題に対して、どれだけ重要であるかを示す部分。複数ある場合は、Sig1, Sig2, 等と表記することもある。",
  )

  await agent.create_term(
	name="固有性",
	synonyms=["UQ", "U", "Uni", "C"],
	description="否定側が、なぜ現状には、プランを導入したときのようなデメリットが無いのかを示す部分。複数ある場合は、UQ1, UQ2, 等と表記することもある。",
  )
  
  await agent.create_term(
	name="発生過程",
	synonyms=["AP", "H"],
	description="否定側が、プランを導入すればなぜデメリットが発生するのかを示す部分。複数ある場合は、AP1, AP2, 等と表記することもある。",
  )
  
  await agent.create_term(
	name="深刻性",
	synonyms=["Imp", "インパクト", "S"],
	description="否定側が、なぜデメリットが問題であるのかを示す部分。複数ある場合は、Imp1, Imp2, 等と表記することもある。",
  )

  await agent.create_term(
	name="オルタナティブ・ジャスティフィケーション",
    synonyms=["オルタナ", "オルタナティブ"],
	description="肯定側が、プランをたくさん出して、その中の一つでも立てば良いという戦略。",
  )

  await agent.create_term(
	name="クリティーク",
	description="そもそもそんな議論をすること自体が不適切であるという主張。",
  )

  await agent.create_term(
	name="資料",
	synonyms=["リソース", "情報源", "参考文献", "エビ", "引用", "エビデンス", "e"],
	description="ディベートにおいて、議論をサポートするために使用される情報源や参考文献のこと。これには、統計データ、研究論文、専門家の意見、ニュース記事などが含まれることが多い。引用の形式は以下のように行われる。\n肩書（例えば立命館大学の清水琢磨教授なら、\"立命館大学 清水\"） その資料の公開された年（例えば2020年なら、\"20\"） \n例: 立命館大学 清水 20\n"
  )

  await agent.create_term(
	name="質疑",
	synonyms=["Q&A", "QnA", "質問", "質問タイム", "Q"],
	description="ディベートにおいて、肯定側立論の後には否定側質疑が、否定側立論の後には肯定側質疑が行われる。",
  )

  await agent.create_term(
	name="第一反駁",
	synonyms=["1反駁", "1R", "ファーストリバットル", "1反"],
	description="ディベートにおいて、肯定側と否定側がそれぞれ一度ずつ行う反駁のこと。",
  )

  
  await agent.create_term(
	name="第二反駁",
	synonyms=["2反駁", "2R", "セカンドリバットル", "2反"],
	description="ディベートにおいて、肯定側否定側それぞれ2回目の反駁のこと。うまい人がやることが多い。まとめ的な要素を含む。",
  )

  await agent.create_term(
	name="応答",
	synonyms=["レスポンス", "反論", "反駁", "アンサー", "A"],
	description="質疑に対して応答すること。立論者が行う。",
  )

  await agent.create_term(
	name="肯定側立論",
	synonyms=["Aff立論", "肯定立論", "アファ立論", "Case", "ケース"],
	description="肯定側の立論。もしくは、肯定側の立論者のこと。肯定側応答者も含む。",
  )

  await agent.create_term(
	name="否定側立論",
	synonyms=["Neg立論", "否定立論", "ネガ立論", "DA"],
	description="否定側の立論。もしくは、否定側の立論者のこと。否定側応答者も含む。",
  )

  await agent.create_term(
	name="肯定側質疑",
	synonyms=["Aff質疑", "肯定質疑", "アファ質疑", "AffQ", "肯定Q", "AQ"],
	description="肯定側の質疑。もしくは、肯定側の質疑者のこと。",
  )

  await agent.create_term(
	name="否定側質疑",
	synonyms=["Neg質疑", "否定質疑", "ネガ質疑", "NegQ", "否定Q", "NQ"],
	description="否定側の質疑。もしくは、否定側の質疑者のこと。",
  )

  await agent.create_term(
	name="肯定側第一立論",
	synonyms=["Aff第一立論", "肯定第一立論", "アファ第一立論", "Aff1", "肯定1", "A1", "1AC"],
	description="二立制において、肯定側の一回目の立論。もしくは、肯定側の一回目の立論者のこと。肯定側第一応答者も含む。",
  )

  await agent.create_term(
	name="否定側第一立論",
	synonyms=["Neg第一立論", "否定第一立論", "ネガ第一立論", "Neg1", "否定1", "N1", "1NC"],
	description="二立制において、否定側の一回目の立論。もしくは、否定側の一回目の立論者のこと。否定側第一応答者も含む。",
  )

  await agent.create_term(
	name="肯定側第二立論",
	synonyms=["Aff第二立論", "肯定第二立論", "アファ第二立論", "Aff2", "肯定2", "A2", "2AC"],
	description="二立制において、肯定側の二回目の立論。もしくは、肯定側の二回目の立論者のこと。肯定側第二応答者も含む。",
  )

  await agent.create_term(
	name="否定側第二立論",
	synonyms=["Neg第二立論", "否定第二立論", "ネガ第二立論", "Neg2", "否定2", "N2", "2NC"],
	description="二立制において、否定側の二回目の立論。もしくは、否定側の二回目の立論者のこと。否定側第二応答者も含む。",
  )

  await agent.create_term(
	name="肯定側第一質疑",
	synonyms=["Aff第一質疑", "肯定第一質疑", "アファ第一質疑", "AffQ1", "肯定Q1", "1AQ"],
	description="二立制において、肯定側の一回目の質疑。否定側第一立論に対して行う。もしくは、肯定側の一回目の質疑者のこと。",
  )

  await agent.create_term(
	name="否定側第一質疑",
	synonyms=["Neg第一質疑", "否定第一質疑", "ネガ第一質疑", "NegQ1", "否定Q1", "1NQ"],
	description="二立制において、否定側の一回目の質疑。肯定側第一立論に対して行う。もしくは、否定側の一回目の質疑者のこと。",
  )

  await agent.create_term(
	name="肯定側第二質疑",
	synonyms=["Aff第二質疑", "肯定第二質疑", "アファ第二質疑", "AffQ2", "肯定Q2", "2AQ"],
	description="二立制において、肯定側の二回目の質疑。否定側第二立論に対して行う。もしくは、肯定側の二回目の質疑者のこと。",
  )

  await agent.create_term(
	name="否定側第二質疑",
	synonyms=["Neg第二質疑", "否定第二質疑", "ネガ第二質疑", "NegQ2", "否定Q2", "2NQ"],
	description="二立制において、否定側の二回目の質疑。肯定側第二立論に対して行う。もしくは、否定側の二回目の質疑者のこと。",
  )

  await agent.create_term(
	name="否定側第一反駁",
	synonyms=["Neg第一反駁", "否定第一反駁", "ネガ第一反駁", "Neg1R", "否定1R", "1NR"],
	description="二立制もしくは一立制において、否定側の一回目の反駁。もしくは、否定側の一回目の反駁者のこと。",
  )

  await agent.create_term(
	name="肯定側第一反駁",
	synonyms=["Aff第一反駁", "肯定第一反駁", "アファ第一反駁", "Aff1R", "肯定1R", "A1R", "1AR"],
	description="二立制もしくは一立制において、肯定側の一回目の反駁。もしくは、肯定側の一回目の反駁者のこと。",
  )

  await agent.create_term(
	name="否定側第二反駁",
	synonyms=["Neg第二反駁", "否定第二反駁", "ネガ第二反駁", "Neg2R", "否定2R", "2NR"],
	description="二立制もしくは一立制において、否定側の二回目の反駁。もしくは、否定側の二回目の反駁者のこと。",
  )

  await agent.create_term(
	name="肯定側第二反駁",
	synonyms=["Aff第二反駁", "肯定第二反駁", "アファ第二反駁", "Aff2R", "肯定2R", "A2R", "2AR"],
	description="二立制もしくは一立制において、肯定側の二回目の反駁。もしくは、肯定側の二回目の反駁者のこと。",
  )
  
  await agent.create_term(
	name="オーソリティ",
	description="資料の信頼性。",
  )

  await agent.create_term(
	name="ターン",
    synonyms=["T", "T/A", "TA", "ターンアラウンド"],
	description="相手の議論を逆手に取ること。例えば、相手の議論が正しいと認めた上で、その議論が実はデメリットを生むというような場合。なお、ターンをする場合、その結果発生するものごとがすでに立証されていなければターンとは認められない。",
  )
  
  await agent.create_term(
	name="ニューアーギュメント",
    synonyms=["New", "NA", "ニューアグ", "ニューアーグ", "ニュー"],
	description="全く新しい議論を持ち出すこと。",
  )

  await agent.create_term(
	name="ボーター",
    synonyms=["Voter", "投票理由"],
	description="どちらかに投票する理由。",
  )
