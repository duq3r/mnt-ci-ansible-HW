# Домашнее задание к занятию "09.05 Teamcity" dev-17_09.05-Teamcity-yakovlev_vs
Teamcity

## Подготовка к выполнению

1. В Ya.Cloud создайте новый инстанс (4CPU4RAM) на основе образа `jetbrains/teamcity-server`
2. Дождитесь запуска teamcity, выполните первоначальную настройку
3. Создайте ещё один инстанс(2CPU4RAM) на основе образа `jetbrains/teamcity-agent`. Пропишите к нему переменную окружения `SERVER_URL: "http://<teamcity_url>:8111"`
4. Авторизуйте агент
5. Сделайте fork [репозитория](https://github.com/aragastmatb/example-teamcity)
6. Создать VM (2CPU4RAM) и запустить [playbook](./infrastructure)

![](pic/YC_teamsity.png)

## Основная часть

#### Решение

1. Создайте новый проект в teamcity на основе fork

Создан новый проект - Netology

2. Сделайте autodetect конфигурации

сделано

3. Сохраните необходимые шаги, запустите первую сборку master'a

Запустил. Прошло успешно
![](pic/11.png)

4. Поменяйте условия сборки: если сборка по ветке `master`, то должен происходит `mvn clean deploy`, иначе `mvn clean test`

![](pic/1.png)

5. Для deploy будет необходимо загрузить [settings.xml](./teamcity/settings.xml) в набор конфигураций maven у teamcity, предварительно записав туда креды для подключения к nexus

![](pic/5.png)

6. В pom.xml необходимо поменять ссылки на репозиторий и nexus

![](pic/6.png)

7. Запустите сборку по master, убедитесь что всё прошло успешно, артефакт появился в nexus

![](pic/7.png)

8. Мигрируйте `build configuration` в репозиторий

![](pic/8.png)

9. Создайте отдельную ветку `feature/add_reply` в репозитории

```bash
❯ git checkout -b feature/add_reply
Switched to a new branch 'feature/add_reply'
```

10. Напишите новый метод для класса Welcomer: метод должен возвращать произвольную реплику, содержащую слово `hunter`

```bash
    public String sayHunter() {
        return "When the first hunter appeared he tought another one.";
	}
```

11. Дополните тест для нового метода на поиск слова `hunter` в новой реплике

```bash
	@Test
    public void netologySaysHunter() {
        assertThat(welcomer.sayHunter(), containsString("hunter"));
    }
```

12. Сделайте push всех изменений в новую ветку в репозиторий

![](pic/10.png)

13. Убедитесь что сборка самостоятельно запустилась, тесты прошли успешно

![](pic/12.png)

14. Внесите изменения из произвольной ветки `feature/add_reply` в `master` через `Merge`

- есть

15. Убедитесь, что нет собранного артефакта в сборке по ветке `master`

![](pic/9.png)

16. Настройте конфигурацию так, чтобы она собирала `.jar` в артефакты сборки

![](pic/13.png)

17. Проведите повторную сборку мастера, убедитесь, что сбора прошла успешно и артефакты собраны

![](pic/14.png)

18. Проверьте, что конфигурация в репозитории содержит все настройки конфигурации из teamcity

- есть

19. В ответ предоставьте ссылку на репозиторий

[Репозиторий example-teamcity](https://github.com/duq3r/example-teamcity)

---