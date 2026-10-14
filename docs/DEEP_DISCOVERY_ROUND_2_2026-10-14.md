# Глубокий поиск: ещё пять проходов — 14 октября 2026

Продолжение [предыдущих пяти проходов](FIVE_PASS_DISCOVERY_2026-10-14.md) для super-gitochek. Цель прежняя: простое осязаемое действие, быстрая видимая награда, понятное улучшение и небольшой объём производства. Оценки ниже — исследовательское суждение о механике и объёме собственной реализации, не прогноз успеха на Яндекс Играх.

## Результат

В короткий список добавляются **Glassbloom** как отдельное ядро «выдувай → отпускай → собирай формы», **COREBREAK** как более дорогой цикл «цель → рычаг → цепочка разрушений → улучшение» и **Beat Foundry** как эксперимент с покупкой слышимого результата. **Copper Scrapper** из предыдущего отчёта остаётся сильным ориентиром простоты: новые находки не отменяют его автоматически.

| Находка | Что стоит изучать | Производственная оценка собственной сокращённой версии | Проверка |
|---|---|---|---|
| Glassbloom | Число вдохов выбирает форму, момент отпускания — качество | Низкая–средняя для изолированного ядра | Обработчики и правила; live заблокирован WebGL в исследовательском браузере |
| COREBREAK | Три действия дают пространственные цепочки и выбор улучшения | Средняя, выше простого кликера | Симуляция, награда, покупка, процедурная графика; live WebGL не запустился |
| Beat Foundry | Покупка добавляет ноту к работающему музыкальному механизму | Средняя; важны аудиотайминг и понятность без звука | Код и короткий живой сеанс до новой партии HAT |
| Rock Fortune | Промывка постепенно открывает заранее выбранные находки | Низкая–средняя только для отдельной 2D-промывки | Обработчики внутри index.html |
| Little Vac | Всасывание → заполнение мешка → разгрузка → завершение работы | Средняя; комнаты и уборка последних частиц увеличивают объём | Код старой версии; актуальная публикация отличается |
| Celadon | Формование и оценка изделия | Высокая для полного цикла | Выбранные обработчики симуляции, оценки и награды |
| Soap Cutting | Срезание подготовленных слоёв открывает подарок | Средняя; физика и подготовка объектов | Четыре C#-скрипта; экономика не подтверждена |
| Leaf Me Alone | Короткая сессия ловли листьев с улучшениями | Низкая–средняя; слабее по новизне | Игрок, менеджер, переходы сессий, часть дерева улучшений |

Проведены **пять направленных проходов**, отправлены **54 разных GitHub-запроса**: 53 завершились успешно, один запрос по автору вернул 422 и при повторе. Просмотрены деревья **28 репозиториев**, плюс README ещё двух проектов автора winchxyz. Глубина различается: от структуры до проверки конкретных обработчиков. Это не 30 проверенных игр и не полный аудит всех файлов. Дополнительно использованы страницы авторов и веб-поиск.

## 1. Промывка, жеоды и скрытая находка

### Rock Fortune — andrewvbro/prospecting-game

[Исходники](https://github.com/andrewvbro/prospecting-game) · [Браузерная версия](https://andrewvbro.github.io/prospecting-game/)

В index.html просмотрены startWash, updatePan и collectPanItem. При начале промывки уже подготовленные находки получают порог washAt. Удержание увеличивает panWash; грязь исчезает, а при пересечении порогов находки автоматически попадают в коллекцию/сумку. Базовая скорость прогресса — 0.42 плюс 0.12 за уровень промывки. Завершённая промывка закрывается с задержкой.

**Полезная деталь:** приятное постепенное обнаружение можно получить без честной физики песка, воды и сортировки камней. Это последовательное раскрытие наград с визуальным слоем. Для прототипа достаточно одного лотка и нескольких силуэтов находок.

Полную игру брать за образец малого производства нельзя: здесь Three.js, передвижение, миры, оборудование, задания и другие системы. Прочитан отдельный цикл; живой сеанс не проводился.

### GEODE SMASH — отдельный веб-референс

[Страница автора](https://mrbongobong.itch.io/geode-smash)

Автор описывает удержание молотка, вскрытие оболочки, извлечение и оценку кристалла. Новые находки занимают полку и дают пассивный доход; дубликаты имеют отдельное применение. Полезное сочетание: краткое разрушение + раскрытие предмета + видимая коллекция.

Публичный исходный код в проведённом поиске не найден. Наличие браузерной демоверсии не означает, что полный проект проверен или дёшев в реализации. Пока это **кандидат на следующий живой разбор**, а не рекомендация кодовой базы.

### Ошибка удачи в другом prospecting-game

В **schurmangrant-ctrl/prospecting-game**, game.js, проверяется `roll - luck <= cumulative`, при этом сначала перечислены обычные находки. Положительная удача расширяет первый интервал. При исходных вероятностях 60/30/10% и luck=0.05 получается 65/30/5%; при luck=0.10 последний интервал исчезает.

Это статический вывод из формулы, не статистический тест. Улучшение, обещающее удачу, фактически ухудшает доступность редкой находки. Сам цикл в этой реализации в основном мгновенно разыгрывает содержимое груза; он слабее Rock Fortune как образец постепенной промывки.

## 2. Сбор, сгребание и уборка

### Little Vac — NathanWNorris/little-vac

[Исходники](https://github.com/NathanWNorris/little-vac) · [Публикация автора](https://fooded.itch.io/little-vac)

В dist/simulation.js проверено не только описание: учитываются радиус и прямая видимость, пыль убирается постепенно, мусор ускоряется к пылесосу с закручиванием, затем подбирается на близком расстоянии. Вместимость мешка ограничена; у дока происходит разгрузка. Работа завершается после сбора всего необходимого мусора. README объясняет отложенную выплату за завершённую работу.

**Различать версии:** README прямо называет репозиторий более ранней версией **1.6.11**. Нынешняя публикация Workshop 2.1+ имеет другой состав помещений и требования к управлению. Нельзя приписывать текущей веб-игре проверенные обработчики старого репозитория или смешивать её числа с README.

Главный риск — производство комнат и утомительный поиск последних частиц. В авторских devlog есть обсуждение повторяемости длинных работ и последующее сокращение/переработка контента. Это полезный сигнал о дизайне, но не показатель рынка. Для нашего масштаба лучше одна область, заметные скопления мусора и короткая понятная разгрузка.

### Leaf Me Alone — Stanlee1234/LeafMeAlone

Игрок двигается по горизонтали, ловит листья и получает валюту. В коде есть золотые листья, временный кофейный бонус скорости/дохода и дополнительные секунды. Контроллер сцены возвращает из ограниченной сессии в пространство улучшений. Часть параметров дерева улучшений задаётся непосредственно в узлах Godot.

Цикл достаточно мал, но управление и падающие объекты делают его обычной игрой на ловлю. Сейчас это запасной вариант, а не новый лидер.

**Остальная очередь:** no-leaves-left подтверждает движение грабель мышью, отдельный поворот и модификатор столкновения; доказанной экономики пока нет. MidnightMower просмотрен по структуре Java/libGDX и генератору уровней. leaf-hunter, capital-fish и oilman_2022 не получили достаточно глубокого подтверждения, чтобы попасть в короткий список.

## 3. Формование, стекло и обработка материала

### Glassbloom — drangoht/glassbloom

[Исходники](https://github.com/drangoht/glassbloom) · [Играть](https://drangoht.itch.io/glassbloom)

Это самая полезная новая находка для **изолированного простого ядра**.

Проверенные правила:
- Начало удержания считается вдохом; удержание увеличивает размер заготовки.
- Число вдохов определяет форму: один — миска, два — ваза, три и больше — колба. Есть второе семейство форм.
- Раннее отпускание позволяет продолжить, а отпускание внутри целевого кольца завершает изделие с оценкой точности.
- В ShapingRules центр кольца 1.6, половина ширины 0.14. Качество даёт множители 1/2/3/5; чрезмерный размер приводит к разрыву и небольшой компенсации.
- CollectionRules задаёт витрину 6 × 8: формы и пигменты, отдельное состояние шедевра, бонус дохода от заполнения.
- В GlassbloomGame проверены переход удержания, отпускание, завершение, начисление и обновление витрины.

Здесь два результата одного управления: **планируешь форму числом вдохов, стараешься получить качество отпусканием**. Это содержательнее обычного удержания до полоски. Цвет при этом выбирается из открытых пигментов случайно: не все характеристики коллекции полностью контролируются.

Собственный первый прототип: одна печь, три формы, несколько цветов, одно кольцо точности, видимая полка и два улучшения. Это предложение объёма, не утверждение о готовой сокращённой сборке. Полные престижи и дальнейшие системы оригинала не нужны для проверки ядра. Стоимости пигментов в исходнике растут очень резко, поэтому оригинальный баланс нельзя автоматически переносить.

**Предел проверки:** live-страница показала «Your browser does not support WebGL». Проверена логика исходников; ощущения от управления и соответствие живой сборки этому коммиту не подтверждены. Unity/URP и присутствие сгенерированных изображений также не дают оснований называть проект игрой без ассетов.

### Celadon — winchxyz/celadon

[Исходники](https://github.com/winchxyz/celadon) · [Демо](https://winchxyz.github.io/celadon/)

В clay.js модель содержит 168 секций материала с внутренним/внешним радиусом, сохранением объёма, влажностью и деформациями. scoring.js оценивает силуэт, качество стенок, глазурь и обжиг; game.js связывает результат с оплатой, репутацией и открытием материалов.

Это не просто деформация картинки. Полный цикл включает формование, сушку/подрезку, глазурь, обжиг и оценку. Просмотрены отдельные значимые участки крупных файлов, не вся симуляция.

**Вывод:** процедурная графика сокращает рисование, но не гарантирует малого инженерного объёма. Для текущего ограничения WoodForm из прошлого отчёта остаётся более узким референсом. Celadon полезен как источник приёмов, полный перенос — HOLD.

### Soap Cutting — TalhaGamga/Unity3D-Soap-Cutting

SoapGenerator группирует подготовленные фрагменты по слоям; активен текущий слой. После его очистки и возврата ножа открывается следующий. Финальный GiftObject поднимается, вращается и запускает эффект. Это проверенный показ спрятанной награды, но цикл валюты и улучшений не подтверждён.

Полезен принцип заранее нарезанных слоёв: произвольное разрушение меша не обязательно. В репозитории есть DinoFracture и готовые сцены/объекты; наличие исходников не делает эти материалы свободными для повторного использования.

В KnifeController ветвление ввода отделяет Editor/Standalone с мышью от остальных платформ с touch. Поведение desktop WebGL требует отдельной проверки: исходный условный код — риск, а не доказанный браузерный баг.

## 4. Рычаги, бурение и короткие машинные циклы

### COREBREAK — Legerdo/COREBREAK

[Исходники](https://github.com/Legerdo/COREBREAK) · [Играть](https://legerdo.github.io/COREBREAK/)

Цель на поле → рычаг → три символа DRILL/BOMB/MAGNET → выполнение действий → руда → покупка одного из трёх улучшений.

В game.ts проверены targetAllowed, canPull, pull, resolveSpin, buy и pick. Покупка списывает стоимость, формирует предложения; выбор повышает уровень улучшения и пересчитывает модификаторы. Первые предложения специально фиксированы: длина бура, газовая цепочка и радиус магнита.

В resolver.ts проверены реальная прочность клеток, разрушение, выдача руды и работа магнита. Часть добычи сразу начисляется, часть остаётся кусочками на поле. Магнит собирает их и взаимодействует с золотом. Соседние одинаковые символы объединяются: DDМ даёт усиленный бур и магнит; DМD сохраняет разделённые действия. Взрывы запускают цепочки.

Важная поправка: **первые два запуска обучающие и заранее заданы**, а сильные комбинации дополнительно страхуются механизмом pity. Раннюю удачную цепочку нельзя интерпретировать как случайное доказательство хорошей частоты наград.

Графика в src/art/sprites.ts строится программно, поле генерируется из распределений слоёв. Но здесь остаются баланс трёх воздействий, очереди эффектов, читаемость цепочек, роботы, fever и финальное ядро. Полный оригинал заметно дороже Copper Scrapper.

Предлагаемый сокращённый объём: один слой, три действия, три типа клеток и несколько улучшений. Роботов и босса добавлять только после проверки первого цикла.

**Технические ограничения:** main.ts явно выбирает Phaser.WEBGL; исследовательский браузер получил «Cannot create WebGL context». Живое управление не проверено. Масштаб вычисляется с нижней границей 1 при базе 640 × 360: узкий мобильный экран требует отдельной адаптации; это вывод из кода, не проведённый мобильный тест.

### Beat Foundry — Legerdo/beat-foundry

[Исходники](https://github.com/Legerdo/beat-foundry) · [Играть](https://legerdo.github.io/beat-foundry/)

Ритмичный удар даёт искры; искры покупают ноты и инструменты; работающий секвенсор приносит доход. В game.ts подтверждены окна попадания, ограничение повторного попадания на тот же бит, начисление, списание при покупке и добавление ноты. Аудиовремя учитывает задержку вывода. Это отдельная техническая задача, хотя графика и звук создаются кодом.

**Короткий живой сеанс:**
1. Запущена печь.
2. Куплена вторая нота KICK: отображаемый доход изменился с 0.4/s на 0.8/s.
3. Зафиксировано одно успешное попадание в обучении (1/4).
4. Открыт HAT за 15 искр, появился новый слой; отображаемый доход стал 2.1/s.

Это ограниченная проверка начала цикла, не прохождение игры. Сам звук инструментами не прослушан, музыкальное качество не оценивается. Счётчик рос и пассивно, поэтому конкретную сумму после серии действий нельзя приписывать только ручным ударам.

Интересно, что награда меняет произведение игрока, а не только число. Для нашей задачи это экспериментальный кандидат: без звука смысл может читаться слабее, а ритмические окна и задержки усложняют реализацию.

## 5. Повторный поиск по авторам, раскрытию предметов и отсев

Новые авторские проекты проверялись отдельно, чтобы не ограничиваться словами incremental/clicker.

- **winchxyz/cut**: cutter.js и slicer.js — геометрическое разрезание, в том числе по свободной траектории. Сильный технический референс, но собственная геометрия и физика не соответствуют обещанию сверхдешёвого прототипа; экономика не подтверждена.
- **winchxyz/tidewright**: процедурные замки из песка и прилив, GPU-симуляция, WebGL2. README и выбранные участки большого game.js. Нельзя объявлять простой игрой только из-за отсутствия рисованных ассетов.
- **winchxyz/seedplot**: инструмент генеративного рисунка, не игра. В critters.js проверено построение симметричных пиксельных существ через маску и seeded RNG. Полезен как отдельный пример удешевления коллекционных изображений; экономики и игрового цикла здесь не заявляем.
- **winchxyz/platen**, **winchxyz/loupe**: README; печатная машинка/инструмент создания сайтов, не искомые игровые циклы.
- **platon-lab/Shredder**: начисление стоимости происходит сразу, затем идут визуальные эффекты; физическое измельчение не подтверждено.
- **sfallmann/shredder**: игра памяти типа Simon, ложное совпадение по названию.
- **syh94jkhdz-debug/Gold-prospecting-game**: по структуре обработчиков это размещение фигур и очистка линий, а не промывка.
- **reciprocal-labs/SpeedPicker**: таймер для физических соревнований по вскрытию замков, не нужная видеоигра.
- **lqt-glitch/Unboxing-lab-game**: учебное сопоставление компьютерных компонентов, не цикл вскрытия случайных наград.
- **sydrit/idleSand**: просмотренная структура с Unity Library не дала пригодного подтверждения исходной игровой логики.

**Веб-референс:** [Plausible Deniability](https://nox-nauta.itch.io/plausible-deniability-cover-your-tracks) описывает разрушение коробок, перенос бумаг в шредер и улучшения. Комментарии о задержках и неудобном совмещении бумаг полезны как напоминание о читаемости сбора и производительности. Исходники не проверены; оценки страницы не являются проверкой спроса.

**Оставлено без рекомендации:** wfairclough/PanningForGold (Racket), Perrien/GemCutting (Swift), Swansonge/incremental-cranker (Playdate), truncator/drill (C++), kitbyfez/neon-vault (частично просмотрен game-system.ts). Структура/начало обработчика не подтверждают полный цикл, поэтому эти позиции нельзя считать найденными удачными играми.

## Что проверять следующим

1. Glassbloom в браузере с работающим WebGL: понятен ли выбор формы без объяснения, насколько приятно отпускание, когда появляется первая новая ячейка коллекции.
2. COREBREAK: читаются ли три действия и награда без перегрузки, сколько времени до первого осмысленного выбора, как работает узкий экран.
3. GEODE SMASH: реальный процесс вскрытия демо, цена производства вариативности камней, скорость получения новой находки.
4. Сравнивать эти циклы с уже проверенным началом Copper Scrapper, а не только между собой.
5. Не расширять мету до подтверждения короткого цикла. В этом проходе рынок Яндекс Игр и коммерческие показатели заново не проверялись.

## Источники и воспроизводимость

Ниже ссылки на зафиксированные коммиты источников. Основные обработчики прочитаны целиком или в контексте функции; крупные файлы просмотрены выборочно. HEAD фиксировался в ходе исследования; соответствие опубликованных веб-сборок этим коммитам не установлено.


### drangoht/glassbloom

Коммит: [62023057c8c76ba8fa73a96571704ee30732b674](https://github.com/drangoht/glassbloom/commit/62023057c8c76ba8fa73a96571704ee30732b674).

- [Assets/Scripts/Rules/ShapingRules.cs](https://github.com/drangoht/glassbloom/blob/62023057c8c76ba8fa73a96571704ee30732b674/Assets/Scripts/Rules/ShapingRules.cs)
- [Assets/Scripts/Rules/CollectionRules.cs](https://github.com/drangoht/glassbloom/blob/62023057c8c76ba8fa73a96571704ee30732b674/Assets/Scripts/Rules/CollectionRules.cs)
- [Assets/Scripts/Gameplay/GlassbloomGame.cs](https://github.com/drangoht/glassbloom/blob/62023057c8c76ba8fa73a96571704ee30732b674/Assets/Scripts/Gameplay/GlassbloomGame.cs)

### Legerdo/COREBREAK

Коммит: [2a457385f9341b5d52aef8220d2812e0fa632531](https://github.com/Legerdo/COREBREAK/commit/2a457385f9341b5d52aef8220d2812e0fa632531).

- [src/sim/game.ts](https://github.com/Legerdo/COREBREAK/blob/2a457385f9341b5d52aef8220d2812e0fa632531/src/sim/game.ts)
- [src/sim/resolver.ts](https://github.com/Legerdo/COREBREAK/blob/2a457385f9341b5d52aef8220d2812e0fa632531/src/sim/resolver.ts)
- [src/data/balance.ts](https://github.com/Legerdo/COREBREAK/blob/2a457385f9341b5d52aef8220d2812e0fa632531/src/data/balance.ts)
- [src/art/sprites.ts](https://github.com/Legerdo/COREBREAK/blob/2a457385f9341b5d52aef8220d2812e0fa632531/src/art/sprites.ts)
- [src/main.ts](https://github.com/Legerdo/COREBREAK/blob/2a457385f9341b5d52aef8220d2812e0fa632531/src/main.ts)
- [src/config.ts](https://github.com/Legerdo/COREBREAK/blob/2a457385f9341b5d52aef8220d2812e0fa632531/src/config.ts)

### Legerdo/beat-foundry

Коммит: [5fd7a4d8cf9f023c08b25432e7b865b4e497ebca](https://github.com/Legerdo/beat-foundry/commit/5fd7a4d8cf9f023c08b25432e7b865b4e497ebca).

- [src/game/game.ts](https://github.com/Legerdo/beat-foundry/blob/5fd7a4d8cf9f023c08b25432e7b865b4e497ebca/src/game/game.ts)
- [src/game/economy.ts](https://github.com/Legerdo/beat-foundry/blob/5fd7a4d8cf9f023c08b25432e7b865b4e497ebca/src/game/economy.ts)

### andrewvbro/prospecting-game

Коммит: [ece85c6b62f51e73d69d3ec574e941492cebff69](https://github.com/andrewvbro/prospecting-game/commit/ece85c6b62f51e73d69d3ec574e941492cebff69).

- [index.html](https://github.com/andrewvbro/prospecting-game/blob/ece85c6b62f51e73d69d3ec574e941492cebff69/index.html)

### winchxyz/celadon

Коммит: [be0342639a28dd92a3ac3169206bede2e18a5116](https://github.com/winchxyz/celadon/commit/be0342639a28dd92a3ac3169206bede2e18a5116).

- [src/sim/clay.js](https://github.com/winchxyz/celadon/blob/be0342639a28dd92a3ac3169206bede2e18a5116/src/sim/clay.js)
- [src/game/scoring.js](https://github.com/winchxyz/celadon/blob/be0342639a28dd92a3ac3169206bede2e18a5116/src/game/scoring.js)
- [src/game/game.js](https://github.com/winchxyz/celadon/blob/be0342639a28dd92a3ac3169206bede2e18a5116/src/game/game.js)
- [src/sim/glaze.js](https://github.com/winchxyz/celadon/blob/be0342639a28dd92a3ac3169206bede2e18a5116/src/sim/glaze.js)

### NathanWNorris/little-vac

Коммит: [f8055967d82e23a788dd16504961eeb74b4d461f](https://github.com/NathanWNorris/little-vac/commit/f8055967d82e23a788dd16504961eeb74b4d461f).

- [README.md](https://github.com/NathanWNorris/little-vac/blob/f8055967d82e23a788dd16504961eeb74b4d461f/README.md)
- [dist/simulation.js](https://github.com/NathanWNorris/little-vac/blob/f8055967d82e23a788dd16504961eeb74b4d461f/dist/simulation.js)
- [dist/progression.js](https://github.com/NathanWNorris/little-vac/blob/f8055967d82e23a788dd16504961eeb74b4d461f/dist/progression.js)
- [dist/world.js](https://github.com/NathanWNorris/little-vac/blob/f8055967d82e23a788dd16504961eeb74b4d461f/dist/world.js)

### TalhaGamga/Unity3D-Soap-Cutting

Коммит: [8be28015b5aef42f78655115764b427d191fe610](https://github.com/TalhaGamga/Unity3D-Soap-Cutting/commit/8be28015b5aef42f78655115764b427d191fe610).

- [Assets/GAME/Scripts/SoapGenerator.cs](https://github.com/TalhaGamga/Unity3D-Soap-Cutting/blob/8be28015b5aef42f78655115764b427d191fe610/Assets/GAME/Scripts/SoapGenerator.cs)
- [Assets/GAME/Scripts/KnifeController.cs](https://github.com/TalhaGamga/Unity3D-Soap-Cutting/blob/8be28015b5aef42f78655115764b427d191fe610/Assets/GAME/Scripts/KnifeController.cs)
- [Assets/GAME/Scripts/GiftObject.cs](https://github.com/TalhaGamga/Unity3D-Soap-Cutting/blob/8be28015b5aef42f78655115764b427d191fe610/Assets/GAME/Scripts/GiftObject.cs)
- [Assets/GAME/Scripts/FractureManager.cs](https://github.com/TalhaGamga/Unity3D-Soap-Cutting/blob/8be28015b5aef42f78655115764b427d191fe610/Assets/GAME/Scripts/FractureManager.cs)

### Stanlee1234/LeafMeAlone

Коммит: [7613cdb3220a0867cdfe4883611b594610478843](https://github.com/Stanlee1234/LeafMeAlone/commit/7613cdb3220a0867cdfe4883611b594610478843).

- [MainGame/player.gd](https://github.com/Stanlee1234/LeafMeAlone/blob/7613cdb3220a0867cdfe4883611b594610478843/MainGame/player.gd)
- [MainGame/GameManager.gd](https://github.com/Stanlee1234/LeafMeAlone/blob/7613cdb3220a0867cdfe4883611b594610478843/MainGame/GameManager.gd)
- [MainGame/scene_controller.gd](https://github.com/Stanlee1234/LeafMeAlone/blob/7613cdb3220a0867cdfe4883611b594610478843/MainGame/scene_controller.gd)
- [UpgradeTree/upgrade_node.gd](https://github.com/Stanlee1234/LeafMeAlone/blob/7613cdb3220a0867cdfe4883611b594610478843/UpgradeTree/upgrade_node.gd)

### schurmangrant-ctrl/prospecting-game

Коммит: [8bda9b3651f02aa6cceb5accea27e8c2103077ea](https://github.com/schurmangrant-ctrl/prospecting-game/commit/8bda9b3651f02aa6cceb5accea27e8c2103077ea).

- [game.js](https://github.com/schurmangrant-ctrl/prospecting-game/blob/8bda9b3651f02aa6cceb5accea27e8c2103077ea/game.js)

### Полный журнал GitHub-запросов

Запрос `user:Legerdo` вернул 422 и при повторе; прямое чтение двух известных репозиториев автора работало. Остальные 53 разные запроса завершились успешно. Дополнительные веб-запросы в этот счёт не входят.

```text
"geode" game
"sifting" game
"prospecting" incremental
"scratching" game
"lockpicking" incremental
"unboxing" game language:JavaScript
"pearl" "incremental"
"excavation" "clicker"
geode game -geometry -geode-sdk in:name,description
prospecting game in:name,description
"lockpicking" game in:name,description
"scratchcard" incremental
"gem cutting" game
"panning" game in:name,description
"harvesting" "incremental" game
"vacuum" game in:name,description
"mowing" game in:name,description
"fishing net" game
"catching" "incremental"
"sweeping" game
"raking" game
"leaf" "incremental"
"pottery" game in:name,description
"glassblowing" game
"pouring" game in:name,description
"forging" incremental in:name,description
"soap" cutting game
"sand" "incremental" game
"juicer" game
"shredding" game
"winding" game in:name,description
"cranking" game in:name,description
"pumping" incremental
"drilling" incremental in:name,description
"stamping" game
"press" "incremental" game
"safe cracking" game
"claw" "incremental" in:readme
"hatching" "incremental" game
"oyster" game in:name,description
"pearl" game in:name,description language:JavaScript
"geode" incremental in:name,description
"scratch" "reveal" game in:name,description
"treasure" "magnet" in:name,description
"demolition" "incremental"
"shredder" game in:name,description
user:NathanWNorris
"glassblowing"
"geode smash"
"shredding" "incremental" in:readme -botupdate -config
user:Legerdo
user:winchxyz
user:drangoht
"panning" "gold" in:readme language:JavaScript -botupdate -config
```

### Репозитории с просмотренным деревом

- [schurmangrant-ctrl/prospecting-game](https://github.com/schurmangrant-ctrl/prospecting-game)
- [andrewvbro/prospecting-game](https://github.com/andrewvbro/prospecting-game)
- [syh94jkhdz-debug/Gold-prospecting-game](https://github.com/syh94jkhdz-debug/Gold-prospecting-game)
- [reciprocal-labs/SpeedPicker](https://github.com/reciprocal-labs/SpeedPicker)
- [Perrien/GemCutting](https://github.com/Perrien/GemCutting)
- [wfairclough/PanningForGold](https://github.com/wfairclough/PanningForGold)
- [lqt-glitch/Unboxing-lab-game](https://github.com/lqt-glitch/Unboxing-lab-game)
- [joedapr0/no-leaves-left](https://github.com/joedapr0/no-leaves-left)
- [nogarcia/leaf-hunter](https://github.com/nogarcia/leaf-hunter)
- [tctree333/capital-fish](https://github.com/tctree333/capital-fish)
- [patschreiber/oilman_2022](https://github.com/patschreiber/oilman_2022)
- [Darkyenus/MidnightMower](https://github.com/Darkyenus/MidnightMower)
- [Stanlee1234/LeafMeAlone](https://github.com/Stanlee1234/LeafMeAlone)
- [winchxyz/celadon](https://github.com/winchxyz/celadon)
- [drangoht/glassbloom](https://github.com/drangoht/glassbloom)
- [sydrit/idleSand](https://github.com/sydrit/idleSand)
- [Legerdo/beat-foundry](https://github.com/Legerdo/beat-foundry)
- [TalhaGamga/Unity3D-Soap-Cutting](https://github.com/TalhaGamga/Unity3D-Soap-Cutting)
- [Swansonge/incremental-cranker](https://github.com/Swansonge/incremental-cranker)
- [Legerdo/COREBREAK](https://github.com/Legerdo/COREBREAK)
- [truncator/drill](https://github.com/truncator/drill)
- [kitbyfez/neon-vault](https://github.com/kitbyfez/neon-vault)
- [NathanWNorris/little-vac](https://github.com/NathanWNorris/little-vac)
- [platon-lab/Shredder](https://github.com/platon-lab/Shredder)
- [sfallmann/shredder](https://github.com/sfallmann/shredder)
- [winchxyz/cut](https://github.com/winchxyz/cut)
- [winchxyz/tidewright](https://github.com/winchxyz/tidewright)
- [winchxyz/seedplot](https://github.com/winchxyz/seedplot)

Исследование ручное: этот документ не означает автоматического одобрения репозиториев. Машинный реестр, код сканера и опубликованные игры в рамках этого прохода не изменялись.
