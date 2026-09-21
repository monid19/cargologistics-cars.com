/* Cargo Logistics — BG / EN translations */
(function () {
  const T = {
    bg: {
      /* ── nav ── */
      'nav.menu':        'Меню',
      'nav.calculator':  'Калкулатор',
      'nav.about':       'За нас',
      'nav.inquiry':     'Запитване',
      /* ── footer ── */
      'footer.home':      'Начало',
      'footer.how':       'Как работи',
      'footer.services':  'Услуги',
      'footer.calculator':'Калкулатор',
      'footer.about':     'За нас',
      'footer.contacts':  'Контакти',
      /* ── INDEX hero ── */
      'hero.korea.title':   'Внос на автомобили<br>от <em>Южна Корея</em>',
      'hero.korea.eyebrow': 'Актуален корейски пазар 2026',
      'hero.korea.track':   'Проследи доставка',
      'hero.korea.encar':   'Избери от Encar.com',
      'hero.china.title':   'Внос на автомобили<br>от <em>Китай</em>',
      'hero.china.eyebrow': 'Актуален китайски пазар 2026',
      'hero.china.guazi':   'Разгледай в Guazi.com',
      'hero.china.autocango':'Разгледай в Autocango.com',
      'hero.desc':    'Пълно съдействие при закупуване и доставка на автомобили от Южна Корея и Китай. Директно до вас, без посредници и без търговска надценка.',
      'hero.promise': '✦ Ние не сме търговци - ние сме вашият партньор ✦',
      'hero.cta':     'Получи оферта',
      'stat.years':   'Години опит',
      'stat.markup':  'Надценка',
      'stat.docs':    'Документация',
      /* ── ticker ── */
      'ticker.1':  'Внос от Корея',
      'ticker.2':  'Внос от Китай',
      'ticker.3':  'Без търговска надценка',
      'ticker.4':  'Варна, България',
      'ticker.5':  'Митнически представител',
      'ticker.6':  '20+ Години опит',
      /* ── cars sections ── */
      'cars.tag.korea':    'Каталог - Корея',
      'cars.tag.china':    'Каталог - Китай',
      'cars.notfound':     'Не намираш каквото търсиш? Виж още обяви в',
      'cars.link.encar':   'Виж в Encar.com →',
      'cars.link.listing': 'Виж обявата →',
      /* ── how it works ── */
      'how.tag':         'Процесът',
      'how.title':       'Как работи?',
      'how.desc':        'Три стъпки са всичко, което трябва да направите. Ние поемаме всичко останало - от инспекцията в Корея до документите за КАТ.',
      'how.s1.title':    'Изберете автомобил от encar.com',
      'how.s1.desc':     'Разгледайте обяви и намерете колата, която харесвате. Може да ни изпратите и бюджет - ще намерим подходящи варианти.',
      'how.s2.title':    'Изпратете ни линка към обявата',
      'how.s2.desc':     'Препратете URL адреса или телефона на продавача. Поемаме цялата комуникация и проверка на автомобила на място в Корея.',
      'how.s3.title':    'Ние се грижим за всичко останало',
      'how.s3.desc':     'Закупуване, контейнер, товарене и укрепване в контейнер, морски транспорт, митница, разтоварване и пълен комплект документи за регистрация в КАТ.',
      /* ── services ── */
      'services.tag':   'Услуги',
      'services.title': 'Какво включва услугата?',
      'services.lead':  'Занимаваме се с целия процес - от комуникацията с продавача в Корея до предаването на документите за регистрация в България.',
      'svc.1': 'Комуникация с търговеца',
      'svc.2': 'Проверка на автомобила на място в Корея',
      'svc.3': 'Вътрешен транспорт до пристанището',
      'svc.4': 'Групиране в контейнер и натоварване',
      'svc.5': 'Морски групажен транспорт',
      'svc.6': 'Обработка на документи в Корея',
      'svc.7': 'Митническо представителство в България',
      'svc.8': 'Документи за регистрация в КАТ',
      /* ── testimonials ── */
      'test.tag':   'Отзиви',
      'test.title': 'Какво казват нашите клиенти',
      'test.1': '"Цялият процес беше изключително гладък - от избора на колата до получаването на документите. Препоръчвам на всеки, който иска кола от Корея!"',
      'test.2': '"Спестих над 3000 EUR в сравнение с местните дилъри. Колата пристигна точно в описаното състояние. Благодаря на екипа на Cargo Logistics!"',
      'test.3': '"Професионално отношение от начало до край. Всичко беше прозрачно - знаех точно за какво плащам. Вече планирам втора кола!"',
      /* ── contact ── */
      'contact.tag':   'Контакти',
      'contact.title': 'Направете запитване',
      'contact.desc':  'Свържете се с нас за подробна разбивка на крайната цена или за да стартирате поръчка. Отговаряме в рамките на 24 часа.',
      'form.name.label':      'Вашето Име',
      'form.name.ph':         'Иван Иванов',
      'form.email.label':     'Email',
      'form.link.label':      'Линк към автомобила',
      'form.link.opt':        '(по желание)',
      'form.link.ph':         'https://www.encar.com/... или просто опишете запитването си',
      'form.budget.label':    'Бюджет (в EUR)',
      'form.budget.opt0':     'Изберете диапазон',
      'form.budget.opt1':     'До 5 000 EUR',
      'form.budget.opt2':     '5 000 - 10 000 EUR',
      'form.budget.opt3':     '10 000 - 20 000 EUR',
      'form.budget.opt4':     'Над 20 000 EUR',
      'form.budget.opt5':     'Само транспорт (вече купена кола)',
      'form.msg.label':       'Допълнителна информация',
      'form.msg.ph':          'Марка, модел, година, специфични изисквания...',
      'form.submit':          'Изпрати Запитване →',
      'form.error':           'Нещо се обърка. Моля, опитайте отново или ни пишете на office@cargologistics-bg.com',
      'form.success.title':   'Запитването е изпратено!',
      'form.success.msg':     'Благодарим ви! Ще се свържем с вас в рамките на 24 часа.',
      /* ── ABOUT page ── */
      'about.hero.eyebrow': 'Нашата история',
      'about.hero.desc':    'Утвърдена българска компания с над 23 години опит в международната логистика, митническото представителство и вноса на автомобили.',
      'about.stat.transparency': 'Прозрачност',
      'about.who.tag':   'Кои сме ние',
      'about.who.title': 'Утвърдени<br>специалисти',
      'about.who.p1':    '<strong>Cargo Logistics</strong> е утвърдена българска компания, специализирана в международната логистика, митническото представителство и търговските операции по внос и износ.',
      'about.who.p2':    'С над 23 години практически опит в сектора, ние предоставяме сигурни, ефективни и професионално организирани решения за бизнеса и частните клиенти.',
      'about.who.p3':    'Работим в пълно съответствие с националното и международното законодателство, като гарантираме коректност, прозрачност и оптимизация на процесите.',
      'about.avc.label':    'Нашият екип',
      'about.avc.headline': 'Висококвалифицирани специалисти с дългогодишна експертиза',
      'about.avc.1': 'Митническо представителство и посредничество',
      'about.avc.2': 'Международна спедиция и логистика',
      'about.avc.3': 'Морски транспорт и контейнерни превози',
      'about.avc.4': 'Внос и износ на стоки',
      'about.avc.5': 'Администриране на международни търговски сделки',
      'about.avc.6': 'Подготовка на търговски и митнически документи',
      'about.exp.tag':   'Компетенции',
      'about.exp.title': 'Областите на нашата<br>експертиза',
      'about.exp.1.title': 'Митническо представителство',
      'about.exp.1.desc':  'Пълно съдействие при митническо оформяне и освобождаване на стоки - навременно, коректно и в съответствие с всички регулации.',
      'about.exp.2.title': 'Морски транспорт',
      'about.exp.2.desc':  'Организация на контейнерни превози и групажни пратки по основните морски маршрути - Азия, Корея, САЩ и Европа.',
      'about.exp.3.title': 'Документация',
      'about.exp.3.desc':  'Подготовка и обработка на всички видове търговски и митнически документи - прецизно и без забавяния.',
      'about.exp.4.title': 'Внос на автомобили',
      'about.exp.4.desc':  'Цялостна организация на процеса по внос на автомобили от Южна Корея, Азия, САЩ и други международни пазари.',
      'about.exp.5.title': 'Международна спедиция',
      'about.exp.5.desc':  'Координация на сложни логистични вериги с надеждни международни партньори и транспортни оператори.',
      'about.exp.6.title': 'Търговско посредничество',
      'about.exp.6.desc':  'Администриране на международни търговски сделки с пълна прозрачност и правна коректност.',
      'about.ci.tag':   'Специализирана услуга',
      'about.ci.title': 'Внос на автомобили',
      'about.ci.lead':  'Една от водещите ни услуги е организирането на цялостен процес по внос на автомобили от международни пазари, включително Южна Корея, Азия, САЩ и други държави.',
      'about.ci.1': 'Консултация и съдействие при избор на автомобил',
      'about.ci.2': 'Организация на международния транспорт, включително морски контейнерен превоз',
      'about.ci.3': 'Проследяване на пратката в реално време',
      'about.ci.4': 'Подготовка и обработка на всички необходими документи',
      'about.ci.5': 'Митническо оформяне и освобождаване на автомобила',
      'about.ci.6': 'Изчисляване на мита, ДДС и допълнителни разходи',
      'about.ci.7': 'Съдействие при регистрация и финализиране на процеса в България',
      'about.ih.title': 'Нашите предимства',
      'about.ih.1': 'Дългогодишен опит в международната търговия и логистика',
      'about.ih.2': 'Сигурен, прозрачен и добре организиран процес',
      'about.ih.3': 'Надеждни международни партньори и транспортни оператори',
      'about.ih.4': 'Конкурентни цени и оптимални срокове за доставка',
      'about.ih.5': 'Индивидуално внимание и персонализирано решение',
      'about.ih.6': 'Поемаме цялата административна и логистична тежест',
      'about.why.tag':   'Защо ние',
      'about.why.title': 'Защо да изберете Cargo Logistics',
      'about.why.desc':  'Cargo Logistics е вашият надежден партньор при международна търговия и внос на автомобили. Ние поемаме цялата административна и логистична тежест, за да осигурим спокойствие и увереност през целия процес.',
      'about.why.1.title': 'Над 23 години доказан опит',
      'about.why.1.desc':  'Дългогодишна практика в международната логистика и митническото представителство.',
      'about.why.2.title': 'Екип от експерти',
      'about.why.2.desc':  'Висококвалифицирани специалисти с дълбока експертиза в международната търговия.',
      'about.why.3.title': 'Пълно обслужване',
      'about.why.3.desc':  'От покупката до получаването - пълен „от врата до врата" сервиз без изненади.',
      'about.why.4.title': 'Коректност и прозрачност',
      'about.why.4.desc':  'Работим в пълно съответствие с националното и международното законодателство.',
      'about.ap.tag':   'Нашият подход',
      'about.ap.title': 'Индивидуален подход към всеки клиент',
      'about.ap.p1':    'Всеки клиент получава индивидуално внимание и персонализирано решение. Ние поемаме цялата административна и логистична тежест, за да осигурим спокойствие и увереност през целия процес.',
      'about.ap.p2':    'Работим с надеждни международни партньори и транспортни оператори, което ни позволява да гарантираме конкурентни цени и оптимални срокове за доставка.',
      'about.ap.quote': 'Cargo Logistics е вашият надежден партньор при международна търговия и внос на автомобили - сигурен, прозрачен и с доказан резултат.',
      'about.cta.title': 'Готови да започнете?',
      'about.cta.desc':  'Свържете се с нас за безплатна консултация и персонализирана оферта.',
      'about.cta.btn':   'Изпрати запитване',
      /* ── CALCULATOR page ── */
      'calc.tag':         'Калкулатор',
      'calc.title':       'Колко ще струва вашата кола?',
      'calc.scp.label':   'Цена на автомобила в Корея',
      'calc.scp.manual':  'Или въведете точна сума (₩):',
      'calc.toggles.label': 'Включи допълнителни разходи:',
      'calc.homologation': 'Хомологация / Технотест',
      'calc.gas':          'Газова уредба',
      'calc.sofia':        'Транспорт до София/Пловдив',
      'calc.sr.label':     'Ориентировъчна крайна цена',
      'calc.sr.note':      'вкл. транспорт, мито и ДДС',
      'calc.sr.car':       'Цена на колата (в EUR)',
      'calc.sr.transport': 'Транспорт & логистика',
      'calc.sr.taxes':     'Мито + ДДС',
      'calc.sr.extras':    'Допълнителни',
      'calc.sr.disclaimer':'* Ориентировъчна стойност. Точната цена зависи от конкретния автомобил.',
      'calc.btn.quote':    'Получи точна оферта →',
      'calc.loading':      'Зарежда…',
      'calc.rate.loading': 'Зарежда курс…',
      'calc.rate.error':   'Курсът е недостъпен',
      /* ── FAQ page ── */
      'faq.breadcrumb.home': 'Начало',
      'faq.breadcrumb.page': 'Често задавани въпроси',
      'faq.h1':   'Често задавани въпроси',
      'faq.lead': 'Всичко, което трябва да знаете преди да поръчате внос на автомобил от Южна Корея.',
      'faq.cat.1': 'Цени и разходи',
      'faq.cat.2': 'Доставка и логистика',
      'faq.cat.3': 'Документи и регистрация',
      'faq.cat.4': 'За услугата',
      'faq.q.1':  'Колко струва вносът на автомобил от Южна Корея?',
      'faq.a.1':  'Крайната цена включва цената на автомобила в Корея, морски транспорт (~1 680 EUR), МИТО, ДДС, за подробно описание на всички разходи може да посетите страницата ни във фейсбук Cargo Logistics Cars. За автомобил на стойност 10 000 EUR общите разходи са приблизително <strong>14 000–15 500 EUR</strong> в зависимост от модела и обема. Използвайте нашия <a href="/calculator">безплатен калкулатор</a> за ориентировъчна сума.',
      'faq.q.2':  'Каква е агентската такса на Cargo Logistics?',
      'faq.a.2':  'Таксата зависи от обема и сложността на услугата. Предоставяме подробна разбивка на всички разходи преди потвърждаване на поръчката - <strong>без скрити такси</strong>. <a href="/#contact">Свържете се с нас</a> за безплатна оферта.',
      'faq.q.3':  'Колко трае доставката от Корея до България?',
      'faq.a.3':  'Морският транспорт от Южна Корея до Варна отнема приблизително 70-80 дни. Към това се добавят 3–7 дни за митническо оформяне и вътрешен транспорт. Общо около <strong>12 седмици</strong> от момента на закупуване на автомобила.',
      'faq.q.4':  'Трябва ли да пътувам до Корея?',
      'faq.a.4':  'Не. Cargo Logistics поема цялата комуникация с продавача, огледа на автомобила на място в Корея, закупуването, товаренето и транспорта. Вие само изпращате линка към обявата в Encar.com и получавате готовия автомобил в България.',
      'faq.q.5':  'Мога ли да проследя доставката си?',
      'faq.a.5':  'Да. Предоставяме проследяване с номера на контейнера. Можете да следите местоположението на пратката в реално време от момента на натоварване до пристигането във Варна.',
      'faq.q.6':  'Какво се случва ако автомобилът е повреден по време на транспорт?',
      'faq.a.6':  'Всички автомобили се транспортират с карго застраховка. При документирана щета по вина на транспортния оператор, застраховката покрива стойността на повредата. Разясняваме условията подробно преди подписването на договора.',
      'faq.q.7':  'Какви документи са нужни за регистрация в КАТ?',
      'faq.a.7':  'Cargo Logistics подготвя всички необходими документи: коносамент (Bill of Lading), инвойс, митническа декларация (ЕАД), сертификат за произход и превод на свидетелството за регистрация. Вие получавате <strong>пълен комплект</strong> за директна регистрация в КАТ.',
      'faq.q.8':  'Как да проверя реалния километраж?',
      'faq.a.8':  'Корейските автомобили могат да бъдат проверени чрез официалния регистър <strong>CarHistory.or.kr</strong> и чрез Encar Diagnosis - услуга за официален технически преглед. Ние извършваме тази проверка за всеки автомобил преди покупката.',
      'faq.q.9':  'Работите ли само с автомобили от Корея?',
      'faq.a.9':  'Не - Cargo Logistics организира внос на автомобили от Южна Корея и Китай. Основната ни специализация е Южна Корея заради достъпния пазар Encar.com и отличното качество на корейските автомобили.',
      'faq.q.10': 'Можете ли да внесете електрически автомобил от Корея?',
      'faq.a.10': 'Да. Внасяме електрически и хибридни автомобили от Корея, включително модели на <strong>Hyundai, Kia и Genesis</strong>. Важно е да се вземе предвид хомологацията - някои модели изискват допълнителна техническа адаптация за ЕС стандарти.',
      'faq.cta.title': 'Не намерихте отговора, който търсите?',
      'faq.cta.desc':  'Свържете се с нас директно. Отговаряме в рамките на 24 часа.',
      'faq.cta.btn':   'Изпрати запитване →',
    },
    en: {
      /* ── nav ── */
      'nav.menu':        'Menu',
      'nav.calculator':  'Calculator',
      'nav.about':       'About',
      'nav.inquiry':     'Inquiry',
      /* ── footer ── */
      'footer.home':      'Home',
      'footer.how':       'How it works',
      'footer.services':  'Services',
      'footer.calculator':'Calculator',
      'footer.about':     'About',
      'footer.contacts':  'Contact',
      /* ── INDEX hero ── */
      'hero.korea.title':   'Car Import<br>from <em>South Korea</em>',
      'hero.korea.eyebrow': 'Current Korean Market 2026',
      'hero.korea.track':   'Track Delivery',
      'hero.korea.encar':   'Browse Encar.com',
      'hero.china.title':   'Car Import<br>from <em>China</em>',
      'hero.china.eyebrow': 'Current Chinese Market 2026',
      'hero.china.guazi':   'Browse Guazi.com',
      'hero.china.autocango':'Browse Autocango.com',
      'hero.desc':    'Full assistance in purchasing and delivering cars from South Korea and China. Directly to you, without middlemen and without commercial markup.',
      'hero.promise': '✦ We are not dealers — we are your partner ✦',
      'hero.cta':     'Get a Quote',
      'stat.years':   'Years of Experience',
      'stat.markup':  'Markup',
      'stat.docs':    'Documentation',
      /* ── ticker ── */
      'ticker.1':  'Import from Korea',
      'ticker.2':  'Import from China',
      'ticker.3':  'No Commercial Markup',
      'ticker.4':  'Varna, Bulgaria',
      'ticker.5':  'Customs Agent',
      'ticker.6':  '20+ Years Experience',
      /* ── cars sections ── */
      'cars.tag.korea':    'Catalog — Korea',
      'cars.tag.china':    'Catalog — China',
      'cars.notfound':     "Can't find what you're looking for? See more listings on",
      'cars.link.encar':   'View on Encar.com →',
      'cars.link.listing': 'View Listing →',
      /* ── how it works ── */
      'how.tag':         'The Process',
      'how.title':       'How does it work?',
      'how.desc':        'Three steps are all you need to do. We handle everything else — from the inspection in Korea to the registration documents.',
      'how.s1.title':    'Choose a car on encar.com',
      'how.s1.desc':     'Browse listings and find the car you like. You can also send us a budget — we\'ll find suitable options.',
      'how.s2.title':    'Send us the listing link',
      'how.s2.desc':     'Forward the URL or the seller\'s contact. We handle all communication and on-site vehicle inspection in Korea.',
      'how.s3.title':    'We take care of everything else',
      'how.s3.desc':     'Purchase, container, loading and securing, sea freight, customs clearance, unloading and a full set of registration documents.',
      /* ── services ── */
      'services.tag':   'Services',
      'services.title': 'What does the service include?',
      'services.lead':  'We handle the entire process — from communication with the seller in Korea to handing over the registration documents in Bulgaria.',
      'svc.1': 'Communication with the Seller',
      'svc.2': 'On-site Vehicle Inspection in Korea',
      'svc.3': 'Inland Transport to the Port',
      'svc.4': 'Container Groupage & Loading',
      'svc.5': 'Sea Freight',
      'svc.6': 'Document Processing in Korea',
      'svc.7': 'Customs Representation in Bulgaria',
      'svc.8': 'Registration Documents',
      /* ── testimonials ── */
      'test.tag':   'Reviews',
      'test.title': 'What our clients say',
      'test.1': '"The whole process was extremely smooth — from choosing the car to receiving the documents. I recommend it to anyone who wants a car from Korea!"',
      'test.2': '"I saved over €3,000 compared to local dealers. The car arrived in exactly the described condition. Thank you to the Cargo Logistics team!"',
      'test.3': '"Professional from start to finish. Everything was transparent — I knew exactly what I was paying for. I\'m already planning a second car!"',
      /* ── contact ── */
      'contact.tag':   'Contact',
      'contact.title': 'Make an Inquiry',
      'contact.desc':  'Contact us for a detailed breakdown of the final price or to start an order. We respond within 24 hours.',
      'form.name.label':      'Your Name',
      'form.name.ph':         'John Smith',
      'form.email.label':     'Email',
      'form.link.label':      'Link to the Vehicle',
      'form.link.opt':        '(optional)',
      'form.link.ph':         'https://www.encar.com/... or just describe your inquiry',
      'form.budget.label':    'Budget (in EUR)',
      'form.budget.opt0':     'Select range',
      'form.budget.opt1':     'Under €5,000',
      'form.budget.opt2':     '€5,000 – €10,000',
      'form.budget.opt3':     '€10,000 – €20,000',
      'form.budget.opt4':     'Over €20,000',
      'form.budget.opt5':     'Transport only (car already purchased)',
      'form.msg.label':       'Additional Information',
      'form.msg.ph':          'Make, model, year, specific requirements...',
      'form.submit':          'Send Inquiry →',
      'form.error':           'Something went wrong. Please try again or email us at office@cargologistics-bg.com',
      'form.success.title':   'Inquiry Sent!',
      'form.success.msg':     'Thank you! We will contact you within 24 hours.',
      /* ── ABOUT page ── */
      'about.hero.eyebrow': 'Our Story',
      'about.hero.desc':    'An established Bulgarian company with over 23 years of experience in international logistics, customs representation, and car imports.',
      'about.stat.transparency': 'Transparency',
      'about.who.tag':   'Who we are',
      'about.who.title': 'Established<br>Specialists',
      'about.who.p1':    '<strong>Cargo Logistics</strong> is an established Bulgarian company specialising in international logistics, customs representation, and import/export trade operations.',
      'about.who.p2':    'With over 23 years of practical experience, we provide secure, efficient and professionally organised solutions for businesses and private clients.',
      'about.who.p3':    'We operate in full compliance with national and international regulations, ensuring correctness, transparency and process optimisation.',
      'about.avc.label':    'Our Team',
      'about.avc.headline': 'Highly qualified specialists with long-standing expertise',
      'about.avc.1': 'Customs representation and brokerage',
      'about.avc.2': 'International freight forwarding and logistics',
      'about.avc.3': 'Sea freight and container transport',
      'about.avc.4': 'Import and export of goods',
      'about.avc.5': 'Administration of international trade transactions',
      'about.avc.6': 'Preparation of commercial and customs documents',
      'about.exp.tag':   'Competencies',
      'about.exp.title': 'Our Areas of<br>Expertise',
      'about.exp.1.title': 'Customs Representation',
      'about.exp.1.desc':  'Full assistance with customs clearance — on time, correctly and in compliance with all regulations.',
      'about.exp.2.title': 'Sea Freight',
      'about.exp.2.desc':  'Container and groupage shipping on major sea routes — Asia, Korea, USA and Europe.',
      'about.exp.3.title': 'Documentation',
      'about.exp.3.desc':  'Preparation and processing of all commercial and customs documents — precisely and without delays.',
      'about.exp.4.title': 'Car Import',
      'about.exp.4.desc':  'Full organisation of the vehicle import process from South Korea, Asia, USA and other international markets.',
      'about.exp.5.title': 'International Freight Forwarding',
      'about.exp.5.desc':  'Coordination of complex logistics chains with reliable international partners and transport operators.',
      'about.exp.6.title': 'Trade Brokerage',
      'about.exp.6.desc':  'Administration of international trade transactions with full transparency and legal correctness.',
      'about.ci.tag':   'Specialist Service',
      'about.ci.title': 'Car Import',
      'about.ci.lead':  'One of our leading services is organising the complete vehicle import process from international markets, including South Korea, Asia, USA and other countries.',
      'about.ci.1': 'Consultation and assistance in choosing a vehicle',
      'about.ci.2': 'Organisation of international transport, including sea container shipping',
      'about.ci.3': 'Real-time shipment tracking',
      'about.ci.4': 'Preparation and processing of all required documents',
      'about.ci.5': 'Customs clearance and release of the vehicle',
      'about.ci.6': 'Calculation of duties, VAT and additional costs',
      'about.ci.7': 'Assistance with registration and finalisation in Bulgaria',
      'about.ih.title': 'Our Advantages',
      'about.ih.1': 'Years of experience in international trade and logistics',
      'about.ih.2': 'Secure, transparent and well-organised process',
      'about.ih.3': 'Reliable international partners and transport operators',
      'about.ih.4': 'Competitive prices and optimal delivery timelines',
      'about.ih.5': 'Individual attention and personalised solutions',
      'about.ih.6': 'We take on all administrative and logistical burden',
      'about.why.tag':   'Why Us',
      'about.why.title': 'Why Choose Cargo Logistics',
      'about.why.desc':  'Cargo Logistics is your reliable partner in international trade and car imports. We take on all administrative and logistical burden to ensure peace of mind throughout the entire process.',
      'about.why.1.title': '23+ Years of Proven Experience',
      'about.why.1.desc':  'Long-standing practice in international logistics and customs representation.',
      'about.why.2.title': 'Team of Experts',
      'about.why.2.desc':  'Highly qualified specialists with deep expertise in international trade.',
      'about.why.3.title': 'Full Service',
      'about.why.3.desc':  'From purchase to delivery — full door-to-door service with no surprises.',
      'about.why.4.title': 'Correctness & Transparency',
      'about.why.4.desc':  'We operate in full compliance with national and international regulations.',
      'about.ap.tag':   'Our Approach',
      'about.ap.title': 'Individual Approach to Every Client',
      'about.ap.p1':    'Every client receives individual attention and a personalised solution. We take on all administrative and logistical burden to ensure peace of mind throughout the entire process.',
      'about.ap.p2':    'We work with reliable international partners and transport operators, allowing us to guarantee competitive prices and optimal delivery timelines.',
      'about.ap.quote': 'Cargo Logistics is your reliable partner in international trade and car imports — secure, transparent and with proven results.',
      'about.cta.title': 'Ready to get started?',
      'about.cta.desc':  'Contact us for a free consultation and personalised quote.',
      'about.cta.btn':   'Send inquiry',
      /* ── CALCULATOR page ── */
      'calc.tag':         'Calculator',
      'calc.title':       'How much will your car cost?',
      'calc.scp.label':   'Car price in Korea',
      'calc.scp.manual':  'Or enter exact amount (₩):',
      'calc.toggles.label': 'Include additional costs:',
      'calc.homologation': 'Homologation / Technical Test',
      'calc.gas':          'Gas Installation',
      'calc.sofia':        'Transport to Sofia / Plovdiv',
      'calc.sr.label':     'Estimated final price',
      'calc.sr.note':      'incl. transport, duty and VAT',
      'calc.sr.car':       'Car price (in EUR)',
      'calc.sr.transport': 'Transport & logistics',
      'calc.sr.taxes':     'Duty + VAT',
      'calc.sr.extras':    'Additional',
      'calc.sr.disclaimer':'* Indicative value. Exact price depends on the specific vehicle.',
      'calc.btn.quote':    'Get exact quote →',
      'calc.loading':      'Loading…',
      'calc.rate.loading': 'Loading rate…',
      'calc.rate.error':   'Rate unavailable',
      /* ── FAQ page ── */
      'faq.breadcrumb.home': 'Home',
      'faq.breadcrumb.page': 'Frequently Asked Questions',
      'faq.h1':   'Frequently Asked Questions',
      'faq.lead': 'Everything you need to know before ordering a car import from South Korea.',
      'faq.cat.1': 'Costs & Pricing',
      'faq.cat.2': 'Delivery & Logistics',
      'faq.cat.3': 'Documents & Registration',
      'faq.cat.4': 'About the Service',
      'faq.q.1':  'How much does it cost to import a car from South Korea?',
      'faq.a.1':  'The final price includes the car price in Korea, sea freight (~€1,680), customs duty, VAT, and our agency fee. For a car worth €10,000 the total costs are approximately <strong>€14,000–€15,500</strong> depending on model and volume. Use our <a href="/calculator">free calculator</a> for an estimate.',
      'faq.q.2':  "What is Cargo Logistics' agency fee?",
      'faq.a.2':  'The fee depends on the volume and complexity of the service. We provide a detailed breakdown of all costs before confirming the order — <strong>no hidden fees</strong>. <a href="/#contact">Contact us</a> for a free quote.',
      'faq.q.3':  'How long does delivery from Korea to Bulgaria take?',
      'faq.a.3':  'Sea freight from South Korea to Varna takes approximately 70–80 days. Add 3–7 days for customs clearance and inland transport. Total approximately <strong>12 weeks</strong> from the time of purchase.',
      'faq.q.4':  'Do I need to travel to Korea?',
      'faq.a.4':  'No. Cargo Logistics handles all communication with the seller, the on-site inspection in Korea, the purchase, loading and transport. You simply send the Encar.com listing link and receive the car in Bulgaria.',
      'faq.q.5':  'Can I track my delivery?',
      'faq.a.5':  'Yes. We provide tracking with the container number. You can monitor the shipment\'s location in real time from loading to arrival in Varna.',
      'faq.q.6':  'What happens if the car is damaged during transport?',
      'faq.a.6':  'All vehicles are transported with cargo insurance. In the case of documented damage caused by the transport operator, the insurance covers the value of the damage. We explain the terms in detail before signing the contract.',
      'faq.q.7':  'What documents are needed for registration?',
      'faq.a.7':  'Cargo Logistics prepares all necessary documents: Bill of Lading, invoice, customs declaration, certificate of origin and a translated registration certificate. You receive a <strong>complete set</strong> for direct registration.',
      'faq.q.8':  'How can I verify the real mileage?',
      'faq.a.8':  'Korean vehicles can be verified through the official registry <strong>CarHistory.or.kr</strong> and via Encar Diagnosis — an official technical inspection service. We perform this check for every vehicle before purchase.',
      'faq.q.9':  'Do you only work with cars from Korea?',
      'faq.a.9':  'No — Cargo Logistics organises vehicle imports from South Korea and China. Our main specialisation is South Korea due to the accessible Encar.com market and the excellent quality of Korean vehicles.',
      'faq.q.10': 'Can you import an electric car from Korea?',
      'faq.a.10': 'Yes. We import electric and hybrid vehicles from Korea, including models from <strong>Hyundai, Kia and Genesis</strong>. Note that some models require additional technical adaptation for EU standards.',
      'faq.cta.title': "Didn't find the answer you're looking for?",
      'faq.cta.desc':  'Contact us directly. We respond within 24 hours.',
      'faq.cta.btn':   'Send inquiry →',
    }
  };

  /* ─── page title map ─── */
  const PAGE_TITLES = {
    bg: {
      '':           'Внос на автомобили от Корея | Cargo Logistics - Варна',
      'index':      'Внос на автомобили от Корея | Cargo Logistics - Варна',
      'about':      'За нас | Cargo Logistics - 23+ години митническа логистика',
      'calculator': 'Калкулатор | Cargo Logistics - Варна',
      'faq':        'Често задавани въпроси - Внос на автомобили от Корея | Cargo Logistics',
    },
    en: {
      '':           'Car Import from Korea | Cargo Logistics - Varna',
      'index':      'Car Import from Korea | Cargo Logistics - Varna',
      'about':      'About Us | Cargo Logistics - 23+ Years Customs Logistics',
      'calculator': 'Calculator | Cargo Logistics - Varna',
      'faq':        'FAQ - Car Import from Korea | Cargo Logistics',
    }
  };

  /* ─── helpers ─── */
  function getLang() {
    return localStorage.getItem('cl-lang') || 'bg';
  }

  function applyLang(lang) {
    document.documentElement.lang = lang;
    localStorage.setItem('cl-lang', lang);

    /* page title */
    const page = location.pathname.replace(/\/$/, '').split('/').pop().replace('.html', '') || '';
    if (PAGE_TITLES[lang][page]) document.title = PAGE_TITLES[lang][page];

    /* text nodes */
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const v = T[lang][el.dataset.i18n];
      if (v !== undefined) el.textContent = v;
    });

    /* innerHTML (contains tags like <br> <em> <strong> <a>) */
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const v = T[lang][el.dataset.i18nHtml];
      if (v !== undefined) el.innerHTML = v;
    });

    /* placeholder attribute */
    document.querySelectorAll('[data-i18n-ph]').forEach(el => {
      const v = T[lang][el.dataset.i18nPh];
      if (v !== undefined) el.placeholder = v;
    });

    /* aria-label attribute */
    document.querySelectorAll('[data-i18n-aria]').forEach(el => {
      const v = T[lang][el.dataset.i18nAria];
      if (v !== undefined) el.setAttribute('aria-label', v);
    });

    /* toggle button label */
    const btn = document.getElementById('lang-toggle');
    if (btn) btn.textContent = lang === 'bg' ? 'EN' : 'BG';

    /* notify page scripts (e.g. calculator) */
    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang } }));
  }

  /* ─── inject toggle button into nav ─── */
  function injectToggle() {
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.id = 'lang-toggle';
    btn.className = 'lang-toggle';
    btn.setAttribute('aria-label', 'Switch language');
    btn.textContent = getLang() === 'bg' ? 'EN' : 'BG';
    btn.addEventListener('click', () => applyLang(getLang() === 'bg' ? 'en' : 'bg'));
    li.appendChild(btn);
    navLinks.appendChild(li);
  }

  /* ─── init ─── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { injectToggle(); applyLang(getLang()); });
  } else {
    injectToggle(); applyLang(getLang());
  }

  /* ─── public API ─── */
  window.i18n = {
    t:         (key) => (T[getLang()][key] ?? T.bg[key] ?? key),
    getLang,
    applyLang,
  };
})();
