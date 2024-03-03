from ..models import Group


# будет использоваться до старта продукта
def distribute_groups(product):
    """
        Распределяет студентов по группам для указанного продукта,
        учитывая ограничения на размеры групп и соблюдая баланс в количестве студентов.
        (разница не более чем в 1 студента)

        Args:
            product (Product): Объект продукта, для которого необходимо распределить студентов.

        Returns:
            list: Список созданных групп для продукта.
        """
    Group.objects.filter(product=product).delete()

    total_students = product.users_with_access.count()
    min_group_size = product.min_group_size
    max_group_size = product.max_group_size

    groups = 0
    remaining_students = total_students
    while True:
        if remaining_students >= min_group_size:
            remaining_students -= min_group_size
            groups += 1
        else:
            break
        if remaining_students <= (max_group_size - min_group_size) * groups:
            break

    created_groups = []
    all_students = list(product.users_with_access.all())
    if groups:
        rest_students = total_students % groups
        for i in range(groups):
            if total_students >= groups * max_group_size:
                group_size = max_group_size
            else:
                group_size = total_students // groups
                if i < rest_students:
                    group_size += 1

            group_students = all_students[:group_size]
            all_students = all_students[group_size:]

            group = Group.objects.create(name=f"Group {i + 1}", product=product)
            group.students.set(group_students)
        created_groups.append(group)

    return created_groups


# будет использоваться после старта продукта
def add_student_to_group(product, student):
    """
        Добавляет студента в одну из групп для указанного продукта,
        учитывая ограничения на размеры групп и соблюдая баланс в количестве студентов.
        (разница не более чем в 1 студента)

        Args:
            product (Product): Объект продукта, в группу которого нужно добавить студента.
            student (User): Объект пользователя, который будет добавлен в группу.

        Returns:
            None
        """
    groups = Group.objects.filter(product=product)
    target_group = min(groups, key=lambda group: group.students.count())
    if target_group.students.count() >= product.max_group_size:
        print('Нет свободных мест в группах. Добавление студента невозможно.')
        return

    target_group.students.add(student)
    print(f'Студент {student.username} успешно добавлен в группу {target_group.name}.')
