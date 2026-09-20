# Не-рыболовные механики — выборочный ручной разбор, 2026-09-20

**Метод:** точечный поиск GitHub по `game jam` + предметным словам (`conveyor belt`, `elevator`, `recycling`, `pawn shop` и др.), чтение README и выбранных исходников. Это **не** ещё один массовый прогон Game Miner и **не** систематическая ревизия всех 236 pending. `data/discovery-registry.json` не изменён. Ни одна игра не запускалась; не проверены живые ощущения, мобильная производительность, права на каждый ассет или спрос в Яндекс Играх. Выводы о собственном MVP ниже — гипотезы, не характеристики оригинальных игр.

## Подтверждённые по коду идеи

### 1. [Beltline Panic](https://github.com/S3-D1/beltline-panic) — необработанная деталь вернётся по кругу

- [Конвейер](https://github.com/S3-D1/beltline-panic/blob/main/src/systems/ConveyorSystem.ts): детали в состоянии `new` проходят выходную развилку и продолжают круг; обработанные выходят на отвод. [ItemSystem](https://github.com/S3-D1/beltline-panic/blob/main/src/systems/ItemSystem.ts) пропускает детали на ленту с учётом безопасных интервалов и завершает забег при переполнении входной очереди/столкновении. [GameManager](https://github.com/S3-D1/beltline-panic/blob/main/src/systems/GameManager.ts) увеличивает скорость ленты и поток деталей по мере времени.
- Важная поправка к «простой фабрике»: [MachineSystem](https://github.com/S3-D1/beltline-panic/blob/main/src/systems/MachineSystem.ts) содержит три станции, последовательности направлений, ёмкости, ожидание безопасного возврата и автоматизацию. **Исходная игра не низкозатратна при полном копировании.** Для собственного исследования выделять одну станцию, один тип предмета, один апгрейд и прозрачный fail state. Это предложение экспериментального среза, не проверенный дизайн.
- [Публичное демо](https://s3-d1.github.io/beltline-panic/) заявлено в README; не запускали. В корневом [LICENSE](https://github.com/S3-D1/beltline-panic/blob/main/LICENSE) — MIT на ПО; отдельное происхождение графики/аудио всё равно требует проверки.

### 2. [The Lying Elevator](https://github.com/Kokomolokolo/the-lying-elevator) — растущие правила пропуска

- [scripts/game.gd](https://github.com/Kokomolokolo/the-lying-elevator/blob/main/scripts/game.gd): случайная внешность гостя, выбор admit/reject, ошибка заканчивает забег, правильное решение добавляет streak. Каждые три гостя появляется новое правило. Словарь старых запретов **не очищается**; но новое правило для того же ключа может перезаписать старое — не путать с безусловным накоплением каждого запрета.
- Интересен малый двухкнопочный контроль под растущей когнитивной нагрузкой. В просмотренном скрипте нет экономики/сильного reward loop: для нашей задачи это механический референс, **не** самостоятельная доказанная opportunity. Права на код/ассеты не проверены.

### 3. [Recycler](https://github.com/EngoDev/recycler) — нацелься на взрывающийся мусор

- [README](https://github.com/EngoDev/recycler/blob/main/README.md): печатать слова на падающем мусоре до пересечения линии поражения; красный предмет взрывается, уничтожая соседей. [trash.rs](https://github.com/EngoDev/recycler/blob/main/src/trash.rs) действительно создаёт взрывной collider и удаляет пересёкшийся мусор. [score.rs](https://github.com/EngoDev/recycler/blob/main/src/score.rs) содержит combo progress/modifier, но без запуска не утверждать, что баланс успешен.
- [typing.rs](https://github.com/EngoDev/recycler/blob/main/src/typing.rs) жёстко перечисляет клавиши A–Z/Backspace: Bevy/Rust-оригинал **не пригоден для прямого мобильного порта**. Возможная самостоятельная идея — определять/нажимать особый предмет, запускающий цепную реакцию, но это уже изменение механики. Не считать готовым браузерным MVP.

### 4. [Rincewind’s Pawn Shop](https://github.com/OniHorns/RincewindsPawnShop) — купил загадочный лот, раскрыл подделку или находку

- [README](https://github.com/OniHorns/RincewindsPawnShop/blob/master/README.md) описывает скупку якобы волшебных вещей у авантюристов. [Customer.cs](https://github.com/OniHorns/RincewindsPawnShop/blob/master/Rincewinds%20Pawnshop/Assets/Scripts/Customer.cs) проверяет предлагаемую цену, выставляет встречную при слишком дешёвом предложении; при покупке списывает цену и добавляет `PawnItem.worth`. [PawnItem.cs](https://github.com/OniHorns/RincewindsPawnShop/blob/master/Rincewinds%20Pawnshop/Assets/Scripts/PawnItem.cs) различает заявленное и настоящее имя; [DialogController.cs](https://github.com/OniHorns/RincewindsPawnShop/blob/master/Rincewinds%20Pawnshop/Assets/Scripts/DialogController.cs) раскрывает вручную прописанный исход.
- Малый предметный сюрприз и риск сделки привлекательны как **отдельная исследовательская гипотеза**, но устойчивый reward loop потребует каталога лотов, честных подсказок, экономики и качественного визуального раскрытия. Это Unity-проект; нет проведённой проверки прав/коммерческого использования. Не переносить исходники и ассеты без проверки.

## Антипримеры и критерии отсечения

- [romualdk/gamedevjs-2026-machines](https://github.com/romualdk/gamedevjs-2026-machines): README обещает интересный обмен «монеты одновременно патроны и деньги на покупки», но фактически выглядит преимущественно как GDD с незавершёнными пунктами; документация упоминает Kontra.js, при этом внутри `vending-machine-mayhem/` лежит Godot-проект. **Идея не подтверждена как реализованная экономика**; не повышать на основании README.
- [yamayuski/gamedevjs-2026-machines](https://github.com/yamayuski/gamedevjs-2026-machines): заявляет 3D-цех на Babylon.js/Havok, демо URL ещё не указан. Это большой physics/3D production burden, не быстрый кандидат.
- Не путать repository search и количество проверенных игровых идей; поиски по некоторым словам дали пустые выдачи и мусор. Проверенные в этой заметке проекты найдены *вне* тройки узких запросов предыдущего эксперимента; их нельзя использовать для вычисления её yield.

## Практический вывод

Из четырёх **не нужно собирать одну игру**. Для быстрых независимых прототипов лучше рассматривать: (a) конвейер с одним пунктом обработки и видимым нарастающим затором; (b) предметный reveal с риском финансового убытка. Лифт — ультрадешёвая проверка двухкнопочного управления, но прежде нужно придумать ощутимую награду; Recycler — прежде решить мобильный input. Никакая находка пока не подтверждает спрос, качество игры или возможность законного переиспользования ассетов.