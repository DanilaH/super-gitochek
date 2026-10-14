# Глубокий поиск, раунд 5 — 14 октября 2026

Продолжение по просьбе «ищи ещё… БООООЛЬШЕЕЕ». Цель прежняя: находить простые игровые действия с заметным результатом и короткой прогрессией для собственных небольших проектов под Яндекс Игры. Это ручное исследование механик, не запуск очередного автоматического Actions-скана.

## Что изменилось

Три главные новые находки: **Bubble Popper**, **Worm Game**, **FisherClicker**. Ещё два полезных направления — **цепная реакция** (два разных исходника) и **язык лягушки с автоматически качающимся прицелом**. Они расширяют набор проверенных механик; прежние Copper Scrapper, Glassbloom, Fossil Fanatic и Field Incremental не отменяются. Рыночного сравнения этих новых игр с Яндекс Играми здесь нет.

| Приоритет | Референс | Что делает игрок | Почему интересен | Главная оговорка |
|---|---|---|---|---|
| A | Bubble Popper | Проводит курсором по пузырям, расширяет зону сбора | Небольшой набор объектов, заметный рост плотности и площади | Hover-ввод требует отдельного решения для телефона |
| A | Worm Game | Разбивает плитку, открывает и забирает червя, покупает помощника | Два последовательных удовольствия: открыть и забрать | Полный зоопарк помощников увеличивает производство арта |
| A− | FisherClicker | Создаёт волну рядом с поплавками, покупает новые поплавки | Одно нажатие даёт массовый улов, размещение имеет смысл | Легендарный финал крайне редок; баланс не переносить |
| B+ | Chain Reaction Incremental / RadioactiveIdle | Выбирает точку запуска каскада, увеличивает плотность и радиус | Много отдачи при минимальном наборе спрайтов | Полная многослойная мета необязательна |
| B+ | Froglick | Нажимает в нужный момент качания прицела, язык возвращает добычу | Награда привязана к возвращению языка; апгрейды меняют действие | Враги, голод, паутина и rage усложняют целую игру |
| B | Blob Chain | Доливает каплю до взрыва и расходится цепочка | Чёткая маленькая головоломка с процедурным полем | Нужны проверка разрешимости и баланс запаса ходов |
| C | Welder | Ведёт горелку по шву | Понятный жест и немедленный визуальный результат | Текущую оценку/завершение нельзя считать надёжными |
| C | ClawMachine | Двигает захват, достаёт капсулу, получает предмет и деньги | Есть реальный цикл наград и улучшений | Физика, коллекция и несколько состояний дороже минимального ядра |

Приоритеты — редакционная оценка пригодности механики и объёма собственной реализации, не рейтинг коммерческого успеха, качества сборки или скорости порта.

## Объём и границы проверки

- Сверены 18 прежних ручных документов, чтобы не выдавать повтор за новую находку.
- Выполнены **100 разных успешных GitHub repository-search запросов**; вместе они вернули 526 строк результатов, включая повторы и нерелевантные проекты. Это не 526 игр.
- Запрошены деревья **43** выбранных репозиториев; получены и просмотрены **42**. У OwenBrush/pixel-pottery дерево получить не удалось.
- Все 42 полученных имени отсутствуют как точные строки в этих 18 документах. Это только «новые имена относительно ручного журнала», не проверка уникальности идеи и не дедупликация всей машинной базы.
- Получены **65 файлов из 30 репозиториев**. Глубина неодинакова: от README и отдельных функций до сквозной проверки ввода, награды и покупки. Таблица ниже явно разделяет уровни.
- SHA всех 65 полученных файлов совпали с соответствующими записями полученных деревьев. Для репозиториев с прочитанными файлами отдельно получены HEAD-коммиты; ссылки ниже закреплены на них.
- Дополнительно выполнены шесть веб-запросов в двух поисковых системах; открыты авторские страницы Worm Game, BubbleByte и Flappuccino. Через ссылку автора Worm Game найден его репозиторий.
- **Ни одной сборки и ни одного live playtest в этом раунде.** Не проверены ощущения, производительность, мобильный ввод, удержание, Yandex SDK и работоспособность целой сборки. Наличие кода не означает, что все сцены и сигналы правильно связаны.
- Автоматическая discovery-registry не менялась. Файлы, полученные для разведки, не исполнялись.

## 1. Bubble Popper — самый компактный новый референс

Репозиторий: https://github.com/w00tyd00d/bubble-popper

**Подтверждённая цепочка:** вход курсора в пузырь → collect → прибавление валюты → исчезновение/звук/всплывающее число → появление в новом месте → покупка.

Сбор обычного пузыря даёт 2 в степени уровня стоимости. Повторное появление начинается после 0,7 секунды ожидания и затем анимируется. Покупка действительно проверяет баланс, вызывает эффект и вычитает цену. Четыре ветки: удвоение числа пузырей, их стоимость, радиус курсора, радужные пузыри. Радиусы после покупок: 8, 16, 24, 32; цены радиуса: 150, 450, 2500, 12500.

Радужный пузырь — не просто другая картинка. Его сбор запускает расширяющуюся волну массового сбора. В container предусмотрены один текущий радужный пузырь и 5-секундная пауза после его сбора. В bubble вероятность попытки сделать пузырь радужным фиксирована: 2/250 после открытия ветки. Не путать с закомментированной старой таблицей вероятностей: повышение уровня меняет множитель награды, а не эту константу.

**Что взять в своё ядро:** один экран, четыре улучшения, разные звуки/масштабы, редкий массовый взрыв. Контентная цена низкая: не нужны десятки уровней и предметов. Для телефона — сознательно спроектировать сбор удержанием и движением пальца; существующий mouse_entered сам по себе не доказывает удобный touch.

Источники: [scripts/bubble.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/bubble.gd), [scripts/game_state.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/game_state.gd), [scripts/shop_button.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/shop_button.gd), [scripts/shop_button_data.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/shop_button_data.gd), [scripts/cursor_area.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/cursor_area.gd), [scripts/bubble_container.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/bubble_container.gd), [scripts/impact_layer.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/impact_layer.gd).

## 2. Worm Game — раскрытие находки плюс отдельный сбор

Авторская страница: https://nekomiya-sebastian.itch.io/worm-game  
Репозиторий: https://github.com/nekomiya-sebastian/worm-game

**Подтверждено по коду:** клик по плитке с индексом больше 1 уменьшает её значение на силу кирки, минимум до 1. Червь становится открытым, когда плитка достигла 1. Его нужно отдельно подобрать кликом; Collect передаёт валюту в shop.GetWorm и ставит флаг collected. Следовательно, добыча и сбор — два разных действия, а не автоматическая выплата за удар.

Начальная плотность червей 0,3; начальный шанс королевского червя задан 0,01. Магазин проверяет число червей, возвращает фактически потраченную цену, а Update вычитает её из баланса. Первый прыгающий тюлень стоит 15 и действительно разрушает плитки при столкновении. Кот доступен от 80 и подбирает уже открытых червей. Отдельно есть сила кирки, плотность, шанс королевского червя и другие помощники.

**Тонкость прогрессии:** полная очистка и сбор всех червей вызывает LoadLevel — повторную загрузку текущего типа поля. NextLevel вызывается отдельным товаром магазина. Нельзя описывать это как автоматический переход на новый биом после каждой очистки. Повышение плотности добавляет 0,2, а не удваивает её, несмотря на изображение x2; королевский шанс увеличивается на 0,08, несмотря на картинку Plus10.

**Что взять:** земля → раскрытие → сбор → один помощник-разрушитель → один помощник-сборщик. Для маленькой своей игры можно заменить червей на самоцветы/монеты, но это наша адаптация, а не найденная версия. Полный набор драконов и лазерных существ на первом этапе не нужен.

Источники: [Scripts/WormMap.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/WormMap.js), [Scripts/MapWorm.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/MapWorm.js), [Scripts/WormShop.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/WormShop.js), [Scripts/BouncingSeal.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/BouncingSeal.js), [Scripts/JumpingCat.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/JumpingCat.js).

## 3. FisherClicker — расставляешь поплавки, запускаешь общую волну

Репозиторий: https://github.com/shademakesgames/FisherClicker

Здесь рыбалка устроена иначе, чем обычные тайминг/поплавок-мини-игры. Щелчок создаёт расходящееся кольцо. Менеджер вычисляет расстояние до каждого поплавка и планирует его on_hit по времени прихода волны. При duration=0,25 и speed=200 начальный охват — строго менее 50 единиц расстояния. Покупка «радиуса» прибавляет 25 к скорости волны; при неизменной длительности это увеличивает её дальность на 6,25.

Попадание действительно начисляет рыбу. Магазин проверяет и списывает отдельные валюты редкости. Можно купить дешёвый поплавок за 100 обычных рыб и поставить его следующей командой ввода. Другие покупки добавляют повторные попадания волны, автоматические волны и поплавки с большим множителем. Получается понятная пространственная петля: больше поплавков в зоне одного импульса → больше отдача.

**Почему не рекомендую переносить исходный финал:** get_fish делает легендарный бросок 1 к 2 000 000. В on_hit число случайных бросков ограничивается десятью, а множитель свыше этого превращается в scale обычного улова. Поэтому поплавок «100000 рыб» не означает 100000 независимых попыток легендарной рыбы. При успехе легендарная выплата остаётся 1. Коллекция из восьми легендарных видов в исходной игре не является доказанно хорошим коротким финалом.

Также менеджер хранит один legendary_fish, так что отображение множества успехов за кадр отдельно не проверено. У начального экрана встречается выражение lock == false вместо присваивания; запуск без игры не утверждаем.

**Что взять:** один пруд, размещаемые поплавки, волна и три улучшения. Для маленького проекта — одна валюта и предсказуемое открытие коллекции вместо многомиллионного ожидания. Это предложение собственной версии.

Источники: [Scenes/game.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scenes/game.gd), [Scripts/ripple_manager.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scripts/ripple_manager.gd), [Scripts/ripple.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scripts/ripple.gd), [Scripts/bobber.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scripts/bobber.gd).

## 4. Цепная реакция — два действительно проверенных варианта

### ChrisE82/chain-reaction-incremental

Нажатие создаёт расширяющуюся область. Активный взрыв задевает соседний idle-шар, который становится следующим источником. triggerBall начисляет coins сразу; endChain отдельно начисляет бонус. После очистки поля есть дополнительный бонус эффективности по числу срабатываний на нажатие, затем восстановление всех принадлежащих игроку шаров.

В store подтверждены проверки достаточности денег и списание при покупке шаров, цветовых улучшений и улучшений нажатия. Цветовые параметры влияют на радиус, длительность, стоимость и другие свойства, а не существуют только в меню. Семь цветовых корзин, длинная статистика и дополнительные системы делают полный проект заметно больше минимального прототипа.

**Короткая версия:** единый тип шаров, радиус/длительность/количество, один запуск и выплата за каскад. Это сильнее как отдельная пространственная механика, чем рядовой кликер по кнопке.

Источники: [src/main.js](https://github.com/ChrisE82/chain-reaction-incremental/blob/4dc5496f5cd724e7ed06b9aa983c83b60471d4bc/src/main.js) (triggerAtPoint, triggerBall, update, endChain), [src/store.js](https://github.com/ChrisE82/chain-reaction-incremental/blob/4dc5496f5cd724e7ed06b9aa983c83b60471d4bc/src/store.js) (tryPurchaseNextBall, tryPurchaseColorUpgrade, tryUpgradeClick, statsFromBucket).

### kolya5544/RadioactiveIdle

Здесь игрок выбирает ближайший атом в зоне указателя. Ball.explode удаляет его, создаёт Explosion и начисляет energy. Explosion.update расширяет область и запускает explode у задетых атомов, передавая общую группу цепочки. Проверена покупка размера, длительности, скорости и числа атомов: баланс проверяется, стоимость вычитается.

Код включает heat/matter/prestige и meltdown. Для нашего запроса это лишние слои, а не аргумент копировать игру целиком. В Mouse touch-обработчики закомментированы — мобильное управление не подтверждено.

Источники: [src/objects/mouse.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/mouse.js), [src/objects/ball.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/ball.js), [src/objects/explosion.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/explosion.js), [src/objects/reactor.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/reactor.js), [src/upgrades.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/upgrades.js).

## 5. Froglick — одна кнопка, качающийся прицел и возврат языка

Репозиторий: https://github.com/Dreamy-Sheeblings/froglick

Прицел автоматически качается по sin(time * sway_speed) в пределах ±75°. Нажатие запускает язык в текущем направлении. При попадании в съедобное насекомое копятся еда, опыт и комбо; после возврата языка состояние DISAPPEAR передаёт эти значения лягушке. Та начисляет очки, сытость и опыт. За промах сбрасывается комбо при соответствующих условиях.

UpgradeManager действительно накапливает опыт, повышает уровень и предлагает до трёх случайных улучшений. Начальный порог 1, далее +2 за уровень; накопление обрезается текущим порогом. В frog.gd подтверждены эффекты: +20% скорости языка за уровень, пробивание, сокращение паузы глотания на 15% за уровень, сила вытягивания из паутины, rage. Это выбор за опыт, не покупка за монеты.

**Что оставить в маленьком прототипе:** качающийся прицел, мухи, возвращающийся язык, три улучшения. Полная версия с паутиной, голодом, жалящими пчёлами и rage дороже. Для полной игры отдельно проверить ограничения накопления апгрейдов и темп голода. Стрекоза передаёт 999999 опыта, но менеджер обрезает его текущим порогом — это не миллион последовательных повышений уровня.

Источники: [scenes/characters/frog/frog.gd](https://github.com/Dreamy-Sheeblings/froglick/blob/197e27c15bbeca1e4fbcf99f9240ef6b036cd903/scenes/characters/frog/frog.gd), [scenes/characters/frog/frog_tongue/frog_tongue.gd](https://github.com/Dreamy-Sheeblings/froglick/blob/197e27c15bbeca1e4fbcf99f9240ef6b036cd903/scenes/characters/frog/frog_tongue/frog_tongue.gd), [scenes/managers/upgrade_manager/upgrade_manager.gd](https://github.com/Dreamy-Sheeblings/froglick/blob/197e27c15bbeca1e4fbcf99f9240ef6b036cd903/scenes/managers/upgrade_manager/upgrade_manager.gd).

## 6. Blob Chain — отдельный puzzle-резерв

Репозиторий: https://github.com/TimGoergen/blob-chain

Нажатие добавляет одну каплю. На пороге 5 blob лопается; четыре капли летят по сторонам света до первой непустой цели, пропуская пустые клетки. Новое столкновение вызывает следующий add_drop. Нажатие на пустую клетку создаёт blob с одной каплей, который тоже придётся убрать.

Поле обычно 6×6, каждый десятый уровень 7×7. Победа — убрать все blobs; проигрыш — исчерпать клики. Main выдаёт дополнительные клики при достижении заданных combo_milestones и переносит остаток с бонусом на следующее поле. Хранится высший достигнутый уровень; это не магазин постоянных апгрейдов.

Важное расхождение комментариев и кода: верхний комментарий Board обещает блокировку ввода во время цепочки, но реальный _process_tap её намеренно не проверяет — новые нажатия разрешены. Это надо учитывать при дальнейшем тесте. Процедурная генерация без прочитанного solver не доказывает разрешимость всех полей.

Источники: [game/core/Blob.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/Blob.gd), [game/core/Board.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/Board.gd), [game/core/LevelManager.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/LevelManager.gd), [game/core/Main.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/Main.gd).

## 7. Welder — жест хороший, текущая реализация требует переработки

Репозиторий: https://github.com/tutut834834/welder

Подтверждены pointer-события, следование горелки за указателем, процедурный путь, оценка расстояния/скорости, искры и повреждение при ошибке. Новые уровни усложняют кривую. Это действительно жест «вести по шву», а не статичная кнопка с тематическим названием.

Но score прибавляется каждый кадр в ветках perfect/good без умножения на dt; нулевая скорость разрешена. Значит стояние на правильной точке потенциально фармит счёт и привязывает его к частоте кадров. progressIndex повышается по индексу ближайшей точки, а не по покрытию всех отрезков; проверка завершения использует этот максимум. Пропуски шва нужно отдельно исключать. Это вывод статического чтения, не воспроизведённый игровой эксплойт.

Для своей версии полезен только сам жест: покрытие сегментов, контроль непрерывности, оплата за завершённую деталь. Наличие магазина в прочитанных обработчиках не подтверждено.

Источник: [index.html](https://github.com/tutut834834/welder/blob/b8f9d860408e0dca3d297bf05fec5ea0ff15cc13/index.html) (makeLevel, qualityNow, gameLoop, onPointerDown, onPointerMove, nextLevel).

## 8. ClawMachine — рабочая связка захват → приз → деньги

Репозиторий: https://github.com/hidelya/ClawMachine

Проверены движение влево/вправо, переход к захвату, прикрепление шара через FixedJoint2D, показ карточки и начисление цены предмета. Удача меняет пороги редкости; скорость действительно умножает горизонтальное движение и спуск на 1,5 после оплаты. Цвет капсулы влияет на множитель выплаты.

Это более дорогой референс, чем пузыри: предметы коллекции, физическая сцена, меню и анимация открытия. В WaitingForCoin после RemoveCoins(1) переход в Moving безусловный, а сама RemoveCoins просто ничего не списывает при нехватке. Это локальное место для проверки; без аудита ButtonState и привязок сцены нельзя утверждать воспроизводимый бесплатный вход.

Источники: [Assets/Scripts/MachineScripts/StateMachine.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/StateMachine.cs), [Assets/Scripts/MachineScripts/MovementPince.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/MovementPince.cs), [Assets/Scripts/MachineScripts/ObjectToPickUp.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/ObjectToPickUp.cs), [Assets/Scripts/MachineScripts/Card.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/Card.cs), [Assets/Scripts/MachineScripts/PlayerStats.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/PlayerStats.cs).

## 9. Отсев, который изменил выводы

**DiggingPirateGame:** 15 кликов по точке в начале, далее требование +5; после завершения выбирается сундук и набор наград, затем новая точка. Но ApplyUpgradeEffect целиком закомментирован. Покупка списывает золото и повышает уровень, не выполняя заявленные эффекты. Поэтому это референс открытия сундука, а не готовой прогрессии. [Assets/Scripts/XSpot.cs](https://github.com/PlaywithK/DiggingPirateGame/blob/a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc/Assets/Scripts/XSpot.cs), [Assets/Scripts/XSpawner.cs](https://github.com/PlaywithK/DiggingPirateGame/blob/a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc/Assets/Scripts/XSpawner.cs), [Assets/Scripts/Upgrades/UpgradeManager.cs](https://github.com/PlaywithK/DiggingPirateGame/blob/a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc/Assets/Scripts/Upgrades/UpgradeManager.cs).

**Tiny Assembly Line:** ресурсы действительно идут ore → plates → gears → credits, покупки и заказы присутствуют. Но ящики на конвейере — CSS-анимация, не объекты с содержимым. Для запроса на тактильную обработку это слабее новой тройки. [index.html](https://github.com/wentaopeng714-cmd/tiny-assembly-line/blob/faecd3f82648761dbb473eaf47e491e41f809d5a/index.html).

**Bouncing Button Incremental:** можно попасть в движущуюся кнопку, увеличить её размер, замедлить и купить автокурсоры/пушки. В выстреле отображается pointsValue * gunMultiplier, а addPoints получает только pointsValue. Это подтверждённое расхождение отображения и начисления, поэтому множитель нельзя описывать как проверенно работающий. [main.js](https://github.com/nowheddos/Bouncing-Button-Incremental/blob/b153d82b5177992bd0d0743dd1557e2a94f1a7c1/main.js), [moveButton.js](https://github.com/nowheddos/Bouncing-Button-Incremental/blob/b153d82b5177992bd0d0743dd1557e2a94f1a7c1/moveButton.js).

**StampmanClicker:** штамп даёт деньги с 100-мс ограничением, изображение опускается и возвращается. В основном классе нет проверенного магазина или смены задания. Как полная новая идея уступает ранее изученному Approved. [MainGame.cs](https://github.com/alex-rusakevich/StampmanClicker/blob/4df1c0a8c59154b55ff750832e24603df2d6ec77/MainGame.cs).

**Punching Bag Incremental:** проверен урон HP, крит при открытой возможности, награда за обнуление HP, возрождение и переход тира. Это честный hit/HP кликер, но без отдельного нового тактильного действия. Магазин в этом проходе не разобран сквозным образом. [main.js](https://github.com/p-u/Punching-Bag-Incremental/blob/ddfa888d632dffd8d8b650a2aef0c169a65e3802/main.js).

**HelloFish** оказался дополнением к WoW, **SweepWeave** — редактором историй, **logicdisaster/vacuum** — пустым README, **sediment** — структурой папок без игровой реализации. Названия не равны механикам.

**mow-town** найден как соседний проект автора ранее известного p-washer: сам README сообщает происхождение. Сочетает стрижку и видимые полосы, но персонаж, 3D-камера, участки, триммер, одежда и видеоповтор выводят целую игру за рамки самого маленького проекта. Это README-отсев по объёму, не проверка всех функций. [README.md](https://github.com/burntsouup/mow-town/blob/0534452de15d7d13f4ba8e56353de6251d840aaf/README.md).

## Веб-ветки и повторы

Авторская страница Worm Game прямо связана с прочитанным репозиторием. BubbleByte по странице автора включает котов-помощников, tower-defense элементы, престиж и множество достижений; здесь это кандидат более крупного масштаба, исходники нужного автора не были установлены. Не подменять их одноимёнными GitHub-репозиториями. https://vittorioromeo.itch.io/bubblebyte

Flappuccino повторно найден через https://polymars.itch.io/flappuccino и поиском GitHub, но PolyMarsDev/Flappuccino уже есть в прежних документах: новой находкой не считается. Аналогично повторно встретились Copper Scrapper, Shuck It, p-washer, Field Incremental, LeafMeAlone, leaf-hunter и ряд старых gold-panning/shredder-кандидатов. Форки и совпадения названий не повышали итоговый список.

## Что проверять следующим

Если нужен следующий этап качества, а не ещё один широкий список: коротко сыграть в Bubble Popper, Worm Game и FisherClicker, измерить время до первого осмысленного улучшения, проверить touch и увидеть, не вырождается ли действие в монотонный сбор. Это ещё не сделано.

Если продолжается именно поиск, отдельная очередь без присвоения качества: ehmorris/bubbles (slingshot/holdBlast по дереву), Mathew-Pearce/Drill-Game, GamerC0der/fallsimulator, shawnxin89/seele-one-button-mining. Дерево не позволяет утверждать их игровые достоинства.

## Полный журнал выбранных кандидатов

Уровень проверки и основание указаны отдельно; каждый ряд не означает глубокий аудит.

| Репозиторий | Результат |
|---|---|
| [ChrisE82/chain-reaction-incremental](https://github.com/ChrisE82/chain-reaction-incremental) | Код цикла и экономики: сильный референс цепной реакции; полная мета избыточна. |
| [kolya5544/RadioactiveIdle](https://github.com/kolya5544/RadioactiveIdle) | Код ввода, взрыва, награды, магазина: брать ядро; heat/matter-прогрессия увеличивает объём. |
| [Eiluce/tilt-and-ink](https://github.com/Eiluce/tilt-and-ink) | Дерево + README: пять столов и сложные правила пинбола; не минимальный проект. |
| [stevo399/bounce](https://github.com/stevo399/bounce) | Дерево + README: многоступенчатая экономика, планеты и престиж; не тактильный минимализм. |
| [nowheddos/Bouncing-Button-Incremental](https://github.com/nowheddos/Bouncing-Button-Incremental) | Код движения, попадания и покупок: резерв; множитель выстрела не совпадает с начислением. |
| [w00tyd00d/bubble-popper](https://github.com/w00tyd00d/bubble-popper) | Сквозной разбор семи скриптов: основной новый кандидат. |
| [rdubrovskis/CornPopper](https://github.com/rdubrovskis/CornPopper) | Фрагменты единственного HTML: обычный числовой кликер; производство попкорна не подтверждено. |
| [renemagitte/incremental-game](https://github.com/renemagitte/incremental-game) | Фрагменты Game.js: счётчик, предметы и диалоги; не подтверждает цепные взрывы. |
| [hidelya/ClawMachine](https://github.com/hidelya/ClawMachine) | Код захвата, состояний, наград и улучшений: полезный резерв, выше цена контента. |
| [Super-Nevyo/One-Button-Fishing](https://github.com/Super-Nevyo/One-Button-Fishing) | CastingManager: прицеливание/заброс/вытягивание/прочность; вся экономика не проверялась. |
| [cleonc13/Water-Fishing](https://github.com/cleonc13/Water-Fishing) | Полный игровой main.js: подводный one-button runner со стрельбой, не спокойная рыбалка. |
| [mk418/HelloFish](https://github.com/mk418/HelloFish) | README: помощник для WoW Classic, не самостоятельная игра. |
| [phantathoang/lasso-catch-godot](https://github.com/phantathoang/lasso-catch-godot) | Код броска и борьбы: клик для лассо, затем частые нажатия клавиш; магазин не подтверждён. |
| [Dreamy-Sheeblings/froglick](https://github.com/Dreamy-Sheeblings/froglick) | Код лягушки, языка и улучшений: сильный one-button референс; полная игра сложнее ядра. |
| [OwenBrush/pixel-pottery](https://github.com/OwenBrush/pixel-pottery) | Дерево получить не удалось; никаких выводов о готовности. |
| [wentaopeng714-cmd/tiny-assembly-line](https://github.com/wentaopeng714-cmd/tiny-assembly-line) | Весь index.html: рабочие числовые преобразования ресурсов; конвейер декоративный. |
| [p-u/Punching-Bag-Incremental](https://github.com/p-u/Punching-Bag-Incremental) | Выборочные функции урона, награды и перехода тира: резерв обычного hit/HP кликера. |
| [Mixygameplay/rock-puncher](https://github.com/Mixygameplay/rock-puncher) | Дерево + README: заявлена ходьба между камнем и магазином; код цикла не разбирался. |
| [logicdisaster/vacuum](https://github.com/logicdisaster/vacuum) | Дерево: только README размером 0; отсеян как пустая заготовка. |
| [k33n42/sediment](https://github.com/k33n42/sediment) | Дерево: README, LICENSE, папки с .gitkeep; игровой реализации не обнаружено. |
| [PlaywithK/DiggingPirateGame](https://github.com/PlaywithK/DiggingPirateGame) | Код раскопок, сундука и магазина: эффекты улучшений закомментированы; не готовая прогрессия. |
| [Mathew-Pearce/Drill-Game](https://github.com/Mathew-Pearce/Drill-Game) | Только дерево: небольшой TS engine/config; остаётся в очереди. |
| [Kammill/the_Peeling](https://github.com/Kammill/the_Peeling) | Только дерево: Rust/Bevy и 3D-модели оружия; механика чистки не подтверждена. |
| [cstepien/sewing_game](https://github.com/cstepien/sewing_game) | piece.py и foot.py: рисование стежков по альфа-маске; in_range пустой, полноценный цикл не подтверждён. |
| [AvramovDV/WeavingGame](https://github.com/AvramovDV/WeavingGame) | Только дерево Unity: уровни, точки, шаги, подсказки; не считать проверенной игрой. |
| [tutut834834/welder](https://github.com/tutut834834/welder) | Функции пути, ввода, оценки, завершения: интересная сварка, но начисление и прогресс требуют переделки. |
| [nekomiya-sebastian/worm-game](https://github.com/nekomiya-sebastian/worm-game) | Пять игровых JS-файлов: добыча → открытие → сбор → помощники; основной кандидат. |
| [Koumarin/vacuum](https://github.com/Koumarin/vacuum) | Только дерево: два скрипта области притяжения; завершённость цикла не проверена. |
| [Ucinorn/snowglobe](https://github.com/Ucinorn/snowglobe) | Только дерево: ресурсы/генераторы/потребители; main.js пуст, готовность не установлена. |
| [GamerC0der/fallsimulator](https://github.com/GamerC0der/fallsimulator) | Только дерево: крупный index.html и minigame; в очередь, без оценки механики. |
| [shawnxin89/seele-one-button-mining](https://github.com/shawnxin89/seele-one-button-mining) | Только дерево: две языковые версии Python; код не проверялся. |
| [FrobozzWaxwing/Sweep_Weave](https://github.com/FrobozzWaxwing/Sweep_Weave) | README: редактор интерактивных историй, ложное попадание по sweep/weave. |
| [ItsMoakey/OrbitSweep](https://github.com/ItsMoakey/OrbitSweep) | Только дерево: 3D FPSController; one-gesture уборка не подтверждена. |
| [opdpinthechat/PopMine](https://github.com/opdpinthechat/PopMine) | Дерево + README: mining/merge/inventory/auras/prestige; объём выше минимального, код не аудитирован. |
| [emanlaw/godot-Coin-Pusher](https://github.com/emanlaw/godot-Coin-Pusher) | GameManager: валюта, достижения, цены монет; физика и полный цикл не проверялись. |
| [shaunhegarty/coin-pusher-godot](https://github.com/shaunhegarty/coin-pusher-godot) | GameController: счётчики, регистрация узлов и сохранение расстановок; физика не проверялась. |
| [shademakesgames/FisherClicker](https://github.com/shademakesgames/FisherClicker) | Четыре игровых скрипта: волна → поплавки → рыба → покупки; основной кандидат с заменой баланса. |
| [TimGoergen/blob-chain](https://github.com/TimGoergen/blob-chain) | Четыре core-скрипта: капли, распространение, лимит ходов, следующий уровень; хороший puzzle-резерв. |
| [AzaleahRaven/Fizzy-Pop-](https://github.com/AzaleahRaven/Fizzy-Pop-) | Только дерево: набор Unity-скриптов; качество механики не установлено. |
| [Sidhant-1024/Claw-Machine-Game](https://github.com/Sidhant-1024/Claw-Machine-Game) | Только дерево: HTML/JS; не приравнивать к разобранному hidelya/ClawMachine. |
| [burntsouup/mow-town](https://github.com/burntsouup/mow-town) | Дерево + README: 3D стрижка, несколько участков, камера/персонаж/одежда; интересный, но более дорогой проект. |
| [ehmorris/bubbles](https://github.com/ehmorris/bubbles) | Дерево + короткий README: уровни, slingshot, holdBlast; отдельная очередь, игровой код не прочитан. |
| [alex-rusakevich/StampmanClicker](https://github.com/alex-rusakevich/StampmanClicker) | MainGame.cs: штамп начисляет деньги, визуально сдвигается; покупки и смена задач не обнаружены в основном классе. |

## Полученные файлы и закрепление источников

Список фиксирует получение файлов. Чтение было выборочным там, где в журнале указаны функции, README или фрагменты; список не следует трактовать как аудит каждой строки.

### kolya5544/RadioactiveIdle

HEAD: `3f581ef58dbe7552eacd35b04e5984af9d379bbf`.

- [README.md](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/README.md) — blob `ca21ed5179ed828a30b370d4ed5c86304fa98c34`.
- [src/objects/ball.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/ball.js) — blob `de4c7c8530515aecc42f76abf546581f1226c1ef`.
- [src/objects/explosion.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/explosion.js) — blob `7a0ecfad8318bddecac57521c6f0af3dbf9d025c`.
- [src/objects/reactor.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/reactor.js) — blob `c6ca7acba23b503b4b279ab194bb1b6727e4e9d1`.
- [src/objects/mouse.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/objects/mouse.js) — blob `b0eefc6536f996dfdeb9ba81869f87f3cb727083`.
- [src/upgrades.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/upgrades.js) — blob `de83e886e5072a5ae4f608cacebb7d50cf15f453`.
- [src/misc/calc_functions.js](https://github.com/kolya5544/RadioactiveIdle/blob/3f581ef58dbe7552eacd35b04e5984af9d379bbf/src/misc/calc_functions.js) — blob `d086fe9439b75a2df1e9a5e3a3abc36f4c3b32f7`.

### w00tyd00d/bubble-popper

HEAD: `ea0355b915c2132dcae1d35fe7121cc91be3eaab`.

- [scripts/bubble.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/bubble.gd) — blob `231bc3e852e3f5072e2c325150bbbb928e4da529`.
- [scripts/game_state.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/game_state.gd) — blob `68efc43aef961fccd380bf6df02d45485f8d251d`.
- [scripts/shop_button.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/shop_button.gd) — blob `844abc565b9cc1a6f8f22c3c6969205344782e65`.
- [scripts/cursor_area.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/cursor_area.gd) — blob `be4f8715513f3ecab36b502d744e9b1eea02209b`.
- [scripts/impact_layer.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/impact_layer.gd) — blob `574495dce55bea6bd6063ec9e722b57cd18d375b`.
- [scripts/bubble_container.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/bubble_container.gd) — blob `11a279f0cd18f7d8c480db7fc78009c9a956339b`.
- [scripts/shop_button_data.gd](https://github.com/w00tyd00d/bubble-popper/blob/ea0355b915c2132dcae1d35fe7121cc91be3eaab/scripts/shop_button_data.gd) — blob `551673218fbcb5f1feb0fdfebd52f98340ce937e`.

### Eiluce/tilt-and-ink

HEAD: `b7c0a98a86ab493c64070c79b786fe935dbd2953`.

- [README.md](https://github.com/Eiluce/tilt-and-ink/blob/b7c0a98a86ab493c64070c79b786fe935dbd2953/README.md) — blob `5cad5d23d46f79e3c20a4a209d554026e06adf0b`.

### stevo399/bounce

HEAD: `b3129767cc4d7ed1967b44898464b94801d82e77`.

- [README.md](https://github.com/stevo399/bounce/blob/b3129767cc4d7ed1967b44898464b94801d82e77/README.md) — blob `e668c55a4208bc3149436af90f0e12ccc0f29f35`.

### cleonc13/Water-Fishing

HEAD: `8545942c43e92633fda9c0aee614fad380bf2607`.

- [docs/onebutton/main.js](https://github.com/cleonc13/Water-Fishing/blob/8545942c43e92633fda9c0aee614fad380bf2607/docs/onebutton/main.js) — blob `ece39931e52713c35d9f6182398cf38082b14c52`.

### phantathoang/lasso-catch-godot

HEAD: `0f267ef31be2108f6c8696df1d0931ad181460e8`.

- [entities/player/player.gd](https://github.com/phantathoang/lasso-catch-godot/blob/0f267ef31be2108f6c8696df1d0931ad181460e8/entities/player/player.gd) — blob `d1ace7586564b46ed383ae9afffba67a3d84ba2d`.
- [systems/game_manager.gd](https://github.com/phantathoang/lasso-catch-godot/blob/0f267ef31be2108f6c8696df1d0931ad181460e8/systems/game_manager.gd) — blob `f14ec897b60b13974746ce0c31a1c6fc6ddb4055`.

### rdubrovskis/CornPopper

HEAD: `f7bd92a353985afb7f6e012f3bdb5069d6f43e18`.

- [CornPopper_v1.0.html](https://github.com/rdubrovskis/CornPopper/blob/f7bd92a353985afb7f6e012f3bdb5069d6f43e18/CornPopper_v1.0.html) — blob `5b861a0d70eb3c64612e01c730138e58447b1a80`.

### wentaopeng714-cmd/tiny-assembly-line

HEAD: `faecd3f82648761dbb473eaf47e491e41f809d5a`.

- [index.html](https://github.com/wentaopeng714-cmd/tiny-assembly-line/blob/faecd3f82648761dbb473eaf47e491e41f809d5a/index.html) — blob `3aba2267097b910447497c0db6cba6b6dffefbb3`.

### Super-Nevyo/One-Button-Fishing

HEAD: `b5c13c77238d0bd81ee3b60b70f437ab8634c11b`.

- [Assets/Scripts/Player/CastingManager.cs](https://github.com/Super-Nevyo/One-Button-Fishing/blob/b5c13c77238d0bd81ee3b60b70f437ab8634c11b/Assets/Scripts/Player/CastingManager.cs) — blob `653f7350fe24aec83485d79725d4c2478e0c2363`.

### PlaywithK/DiggingPirateGame

HEAD: `a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc`.

- [Assets/Scripts/XSpot.cs](https://github.com/PlaywithK/DiggingPirateGame/blob/a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc/Assets/Scripts/XSpot.cs) — blob `4240371e47a9819f63ca72d692e529470aa70b5f`.
- [Assets/Scripts/XSpawner.cs](https://github.com/PlaywithK/DiggingPirateGame/blob/a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc/Assets/Scripts/XSpawner.cs) — blob `4119e66a414e9a3705d0de925dc99514a408fbaf`.
- [Assets/Scripts/Upgrades/UpgradeManager.cs](https://github.com/PlaywithK/DiggingPirateGame/blob/a5a5435c4d77a1cc80378f0dcd30dd7a49ced0dc/Assets/Scripts/Upgrades/UpgradeManager.cs) — blob `674d8f6f8e58ad9477e53c2a19a50035734eb5ac`.

### Dreamy-Sheeblings/froglick

HEAD: `197e27c15bbeca1e4fbcf99f9240ef6b036cd903`.

- [scenes/characters/frog/frog_tongue/frog_tongue.gd](https://github.com/Dreamy-Sheeblings/froglick/blob/197e27c15bbeca1e4fbcf99f9240ef6b036cd903/scenes/characters/frog/frog_tongue/frog_tongue.gd) — blob `173dc79bfab0c5e2868c42026abdd6890fda6338`.
- [scenes/managers/upgrade_manager/upgrade_manager.gd](https://github.com/Dreamy-Sheeblings/froglick/blob/197e27c15bbeca1e4fbcf99f9240ef6b036cd903/scenes/managers/upgrade_manager/upgrade_manager.gd) — blob `e30f5a5029b78226284e157dd5be8924e8e69e00`.
- [scenes/characters/frog/frog.gd](https://github.com/Dreamy-Sheeblings/froglick/blob/197e27c15bbeca1e4fbcf99f9240ef6b036cd903/scenes/characters/frog/frog.gd) — blob `396b1f029fc426f449bde9a6d7e3656971ae3f20`.

### cstepien/sewing_game

HEAD: `4681021cd762cb4b68f6978f5483e022bbf48c32`.

- [piece.py](https://github.com/cstepien/sewing_game/blob/4681021cd762cb4b68f6978f5483e022bbf48c32/piece.py) — blob `6307f49521a9ef316657aef26f6b996b2e4246a4`.
- [foot.py](https://github.com/cstepien/sewing_game/blob/4681021cd762cb4b68f6978f5483e022bbf48c32/foot.py) — blob `deb901a7b04edaf5fdb3fa936ca546f7d41881a4`.

### nekomiya-sebastian/worm-game

HEAD: `558d6ac5c5d28b28a1943346280ac37d14c1aa76`.

- [Scripts/WormMap.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/WormMap.js) — blob `b301fdb0d3268aa71c72db4cde54b48e43924e44`.
- [Scripts/WormShop.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/WormShop.js) — blob `6b18867b631f93c9c096359fc5ad5d977fde0690`.
- [Scripts/MapWorm.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/MapWorm.js) — blob `b127db2f09ca0b5073f48d80a54718b839d24e63`.
- [Scripts/BouncingSeal.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/BouncingSeal.js) — blob `8a934e83d2c2c6e82d6eae514d3f581675757ace`.
- [Scripts/JumpingCat.js](https://github.com/nekomiya-sebastian/worm-game/blob/558d6ac5c5d28b28a1943346280ac37d14c1aa76/Scripts/JumpingCat.js) — blob `76b93cdb346ac409cf0bfc02cc7dc6654377e562`.

### ChrisE82/chain-reaction-incremental

HEAD: `4dc5496f5cd724e7ed06b9aa983c83b60471d4bc`.

- [src/main.js](https://github.com/ChrisE82/chain-reaction-incremental/blob/4dc5496f5cd724e7ed06b9aa983c83b60471d4bc/src/main.js) — blob `83ef83ada950923bfe6ba802d5f99495cc19db38`.
- [src/store.js](https://github.com/ChrisE82/chain-reaction-incremental/blob/4dc5496f5cd724e7ed06b9aa983c83b60471d4bc/src/store.js) — blob `2804f101d889d161da180603ebf1debd8b12252b`.

### nowheddos/Bouncing-Button-Incremental

HEAD: `b153d82b5177992bd0d0743dd1557e2a94f1a7c1`.

- [main.js](https://github.com/nowheddos/Bouncing-Button-Incremental/blob/b153d82b5177992bd0d0743dd1557e2a94f1a7c1/main.js) — blob `db328be3d96334e92428591cf92f63a3a24a2cfd`.
- [moveButton.js](https://github.com/nowheddos/Bouncing-Button-Incremental/blob/b153d82b5177992bd0d0743dd1557e2a94f1a7c1/moveButton.js) — blob `c1dc993e394908307b7c976b05e40e141e75dbbb`.

### tutut834834/welder

HEAD: `b8f9d860408e0dca3d297bf05fec5ea0ff15cc13`.

- [index.html](https://github.com/tutut834834/welder/blob/b8f9d860408e0dca3d297bf05fec5ea0ff15cc13/index.html) — blob `87940457f98db2bc0f1e66c01577c70e54071feb`.
- [README.md](https://github.com/tutut834834/welder/blob/b8f9d860408e0dca3d297bf05fec5ea0ff15cc13/README.md) — blob `064ca1eca4f0f4b8765a5ac3c7afd94042906067`.

### hidelya/ClawMachine

HEAD: `7b8acc3b2d05b95881f70169f73c89b2eea15603`.

- [Assets/Scripts/MachineScripts/StateMachine.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/StateMachine.cs) — blob `3c34ca93418c86e60f7d696da9a8ade721a91fa5`.
- [Assets/Scripts/MachineScripts/PlayerStats.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/PlayerStats.cs) — blob `8ec8e2c232b690377434337bb7f6c3dc990ddf4d`.
- [Assets/Scripts/MachineScripts/Card.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/Card.cs) — blob `7097de4abcd9d16fc8139559847e0decfbc2e5ed`.
- [Assets/Scripts/MachineScripts/MovementPince.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/MovementPince.cs) — blob `004cb7b6ae32362c73677542a148cdfd0461e992`.
- [Assets/Scripts/MachineScripts/ObjectToPickUp.cs](https://github.com/hidelya/ClawMachine/blob/7b8acc3b2d05b95881f70169f73c89b2eea15603/Assets/Scripts/MachineScripts/ObjectToPickUp.cs) — blob `f3d264afa919daf66abf148d1506d103e97078b9`.

### shademakesgames/FisherClicker

HEAD: `28987aa47788bdd057962fe16d14a6c0e286c6e3`.

- [Scenes/game.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scenes/game.gd) — blob `a59e8022da0805b8b94f4dc9471329c8cb0b09b3`.
- [Scripts/bobber.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scripts/bobber.gd) — blob `c743875290ae80b0c621995b725f4f105e674906`.
- [Scripts/ripple_manager.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scripts/ripple_manager.gd) — blob `6a451455fb63f8277182d494ed316bc3a09cf76d`.
- [Scripts/ripple.gd](https://github.com/shademakesgames/FisherClicker/blob/28987aa47788bdd057962fe16d14a6c0e286c6e3/Scripts/ripple.gd) — blob `79664cc850359a0527d6948d15221d0ce5f324b7`.

### TimGoergen/blob-chain

HEAD: `f34d25a4134662da5c93d426df98157a2fd0e669`.

- [game/core/Blob.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/Blob.gd) — blob `ec3faa1fcb2ba896fe8c393e392e8f9108bb3152`.
- [game/core/Board.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/Board.gd) — blob `11b5e489fbf3a69f070f576a55bee52291eff4fe`.
- [game/core/LevelManager.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/LevelManager.gd) — blob `5617b9e3f144d24ca5aefb607384f8a29a77438c`.
- [game/core/Main.gd](https://github.com/TimGoergen/blob-chain/blob/f34d25a4134662da5c93d426df98157a2fd0e669/game/core/Main.gd) — blob `57f2d2cb057641b03a1189a4dc35caaafcaa30f8`.

### burntsouup/mow-town

HEAD: `0534452de15d7d13f4ba8e56353de6251d840aaf`.

- [README.md](https://github.com/burntsouup/mow-town/blob/0534452de15d7d13f4ba8e56353de6251d840aaf/README.md) — blob `c95e95f38564499d49ce8585e35dd32573eab7da`.

### ehmorris/bubbles

HEAD: `5048073e2673914724e1e3946342def9ba2fee07`.

- [README.md](https://github.com/ehmorris/bubbles/blob/5048073e2673914724e1e3946342def9ba2fee07/README.md) — blob `dc520ac79b883cc65305f043b6f4f40636b69a51`.

### FrobozzWaxwing/Sweep_Weave

HEAD: `631c9819ffa32014610f2424f26d7d510ae71f84`.

- [README.md](https://github.com/FrobozzWaxwing/Sweep_Weave/blob/631c9819ffa32014610f2424f26d7d510ae71f84/README.md) — blob `2a1904ddd0024fddddd33e090ec0f3ed6e6a506b`.

### mk418/HelloFish

HEAD: `609810181c00394aac3ceec6238357761f304417`.

- [README.md](https://github.com/mk418/HelloFish/blob/609810181c00394aac3ceec6238357761f304417/README.md) — blob `e2c789c5ac59c116414caad15c061572a1d6b43f`.

### emanlaw/godot-Coin-Pusher

HEAD: `cb08cba8f07f52d484088f2c9fc23a4601eb241f`.

- [scripts/GameManager.gd](https://github.com/emanlaw/godot-Coin-Pusher/blob/cb08cba8f07f52d484088f2c9fc23a4601eb241f/scripts/GameManager.gd) — blob `21c04dc1ac32e4c263ab20e00cb8a2a2f0395531`.

### shaunhegarty/coin-pusher-godot

HEAD: `0eeac3c0ec8f646772a7c17c83c21d057de98268`.

- [Core/Global/game_controller.gd](https://github.com/shaunhegarty/coin-pusher-godot/blob/0eeac3c0ec8f646772a7c17c83c21d057de98268/Core/Global/game_controller.gd) — blob `4ee1a224ee1fcc3209572f4ddd14a5f8289cc470`.

### renemagitte/incremental-game

HEAD: `650775f7c9affaf620473da62f745984a9193ad3`.

- [src/components/Game.js](https://github.com/renemagitte/incremental-game/blob/650775f7c9affaf620473da62f745984a9193ad3/src/components/Game.js) — blob `d76272b9e7549abe38d462b77bfd60d97d03c147`.

### p-u/Punching-Bag-Incremental

HEAD: `ddfa888d632dffd8d8b650a2aef0c169a65e3802`.

- [main.js](https://github.com/p-u/Punching-Bag-Incremental/blob/ddfa888d632dffd8d8b650a2aef0c169a65e3802/main.js) — blob `eabb87d70d07ef296f7d3eb2474d448cc5b748f4`.

### Mixygameplay/rock-puncher

HEAD: `a7c874cf63b2391768a5f614b889d3ab4bd5a605`.

- [README.md](https://github.com/Mixygameplay/rock-puncher/blob/a7c874cf63b2391768a5f614b889d3ab4bd5a605/README.md) — blob `69c5e6c184820df7c90e824842fabbd09624622f`.

### opdpinthechat/PopMine

HEAD: `ca9babc525271b09a34759bae486c6d3f2817d32`.

- [README.md](https://github.com/opdpinthechat/PopMine/blob/ca9babc525271b09a34759bae486c6d3f2817d32/README.md) — blob `605fd8b6f114a381164a625d982217f0a68409f0`.

### alex-rusakevich/StampmanClicker

HEAD: `4df1c0a8c59154b55ff750832e24603df2d6ec77`.

- [MainGame.cs](https://github.com/alex-rusakevich/StampmanClicker/blob/4df1c0a8c59154b55ff750832e24603df2d6ec77/MainGame.cs) — blob `354ab04974aacb184fc38542d4e5f2b40ba087b2`.

## Воспроизводимые поисковые запросы

100 разных запросов, первая страница выдачи, до 8–10 репозиториев на запрос. Это ограниченная выборка, не исчерпывающий обход GitHub. Пустые и нерелевантные выдачи сохранены как часть метода, а не как найденные игры.

1. `"chain reaction" incremental` — 4 строк выдачи.
2. `"explosions" incremental game` — 0 строк выдачи.
3. `"pinball" incremental` — 3 строк выдачи.
4. `"bouncing" incremental` — 10 строк выдачи.
5. `"domino" incremental` — 10 строк выдачи.
6. `"demolition" game godot` — 0 строк выдачи.
7. `"bomb" incremental game` — 5 строк выдачи.
8. `"pop" incremental game` — 10 строк выдачи.
9. `"ricochet" incremental` — 0 строк выдачи.
10. `"avalanche" incremental` — 2 строк выдачи.
11. `"claw" incremental game` — 1 строк выдачи.
12. `"hook" incremental game` — 2 строк выдачи.
13. `"fishing" "one button"` — 3 строк выдачи.
14. `"net" "catching" game` — 6 строк выдачи.
15. `"magnet fishing" game` — 5 строк выдачи.
16. `"spear" incremental` — 0 строк выдачи.
17. `"lasso" game godot` — 1 строк выдачи.
18. `"grabber" game` — 10 строк выдачи.
19. `"crane" incremental` — 10 строк выдачи.
20. `"catching bugs" game` — 10 строк выдачи.
21. `"assembly" "incremental" game` — 8 строк выдачи.
22. `"forging" "clicker" game` — 1 строк выдачи.
23. `"pottery" game godot` — 1 строк выдачи.
24. `"welding" game` — 8 строк выдачи.
25. `"sewing" game` — 8 строк выдачи.
26. `"weaving" game` — 8 строк выдачи.
27. `"embroidery" game` — 7 строк выдачи.
28. `"sticker" "incremental"` — 6 строк выдачи.
29. `"printing" game godot` — 3 строк выдачи.
30. `"sandwich" "assembly" game` — 1 строк выдачи.
31. `"peeling" game` — 8 строк выдачи.
32. `"scratch" "reveal" game` — 8 строк выдачи.
33. `"stamp" game godot` — 1 строк выдачи.
34. `"punch" "incremental"` — 8 строк выдачи.
35. `"shredder" game` — 8 строк выдачи.
36. `"slicing" "incremental"` — 8 строк выдачи.
37. `"sorting" "incremental"` — 8 строк выдачи.
38. `"sanding" game` — 8 строк выдачи.
39. `"polishing" game` — 8 строк выдачи.
40. `"packing" "incremental"` — 3 строк выдачи.
41. `"incremental" "vacuum"` — 3 строк выдачи.
42. `"incremental" "paint"` — 8 строк выдачи.
43. `"incremental" "harvest"` — 8 строк выдачи.
44. `"incremental" "drill"` — 8 строк выдачи.
45. `"incremental" "digging"` — 5 строк выдачи.
46. `"incremental" "laser"` — 8 строк выдачи.
47. `"incremental" "balloon"` — 8 строк выдачи.
48. `"incremental" "snow"` — 8 строк выдачи.
49. `"incremental" "mowing"` — 0 строк выдачи.
50. `"incremental" "crusher"` — 8 строк выдачи.
51. `"incremental" "sieve"` — 1 строк выдачи.
52. `"incremental" "raking"` — 5 строк выдачи.
53. `"incremental" "washing"` — 0 строк выдачи.
54. `"incremental" "scraping"` — 8 строк выдачи.
55. `"incremental" "unpacking"` — 8 строк выдачи.
56. `"vacuum" game godot` — 1 строк выдачи.
57. `"polishing" game in:name,description` — 8 строк выдачи.
58. `"sandpaper" game` — 0 строк выдачи.
59. `"balloon" "incremental" game` — 2 строк выдачи.
60. `"laser" "incremental" game` — 8 строк выдачи.
61. `"snow" "incremental" game` — 2 строк выдачи.
62. `"bubblebyte"` — 8 строк выдачи.
63. `"flappuccino"` — 8 строк выдачи.
64. `"worm" incremental game` — 2 строк выдачи.
65. `"pegs" incremental game` — 0 строк выдачи.
66. `"mining" "one button"` — 1 строк выдачи.
67. `"sorting" "incremental" game` — 8 строк выдачи.
68. `"mowing" game godot` — 2 строк выдачи.
69. `"leaf" incremental game` — 4 строк выдачи.
70. `"sweep" game godot` — 8 строк выдачи.
71. `"rope" "incremental" game` — 0 строк выдачи.
72. `"gumball" game` — 8 строк выдачи.
73. `"coin pusher" godot` — 2 строк выдачи.
74. `"claw" game javascript` — 8 строк выдачи.
75. `"hammer" "incremental" game` — 2 строк выдачи.
76. `"magnet" "incremental" game` — 0 строк выдачи.
77. `"plucking" game` — 8 строк выдачи.
78. `"unravel" game godot` — 1 строк выдачи.
79. `"wrapping" game godot` — 3 строк выдачи.
80. `"rub" "incremental" game` — 2 строк выдачи.
81. `"washing" game javascript` — 4 строк выдачи.
82. `"screw" game godot` — 3 строк выдачи.
83. `"cutting" "game jam"` — 5 строк выдачи.
84. `"popping" "game jam"` — 8 строк выдачи.
85. `"chain reaction" game godot` — 8 строк выдачи.
86. `"stamp" "clicker"` — 8 строк выдачи.
87. `"bubble wrap" game` — 8 строк выдачи.
88. `"satisfying" game godot` — 5 строк выдачи.
89. `"satisfying" game javascript` — 8 строк выдачи.
90. `"reveal" "incremental" game` — 8 строк выдачи.
91. `"excavation" game` — 8 строк выдачи.
92. `"dig" "game jam"` — 8 строк выдачи.
93. `"crank" game` — 8 строк выдачи.
94. `"scrubbing" game` — 8 строк выдачи.
95. `"panning" game gold` — 8 строк выдачи.
96. `"geode" game` — 8 строк выдачи.
97. `"shucking" game` — 3 строк выдачи.
98. `"stencil" game` — 8 строк выдачи.
99. `"slicing" game godot` — 8 строк выдачи.
100. `"unboxing" game godot` — 1 строк выдачи.
