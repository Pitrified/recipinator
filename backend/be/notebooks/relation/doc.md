
`sqlalchemy/orm/relationships.py`:

```
:param foreign_keys:

    A list of columns which are to be used as "foreign key"
    columns, or columns which refer to the value in a remote
    column, within the context of this :func:`_orm.relationship`
    object's :paramref:`_orm.relationship.primaryjoin` condition.
    That is, if the :paramref:`_orm.relationship.primaryjoin`
    condition of this :func:`_orm.relationship` is ``a.id ==
    b.a_id``, and the values in ``b.a_id`` are required to be
    present in ``a.id``, then the "foreign key" column of this
    :func:`_orm.relationship` is ``b.a_id``.

    In normal cases, the :paramref:`_orm.relationship.foreign_keys`
    parameter is **not required.** :func:`_orm.relationship` will
    automatically determine which columns in the
    :paramref:`_orm.relationship.primaryjoin` condition are to be
    considered "foreign key" columns based on those
    :class:`_schema.Column` objects that specify
    :class:`_schema.ForeignKey`,
    or are otherwise listed as referencing columns in a
    :class:`_schema.ForeignKeyConstraint` construct.
    :paramref:`_orm.relationship.foreign_keys` is only needed when:

    1. There is more than one way to construct a join from the local
        table to the remote table, as there are multiple foreign key
        references present.  Setting ``foreign_keys`` will limit the
        :func:`_orm.relationship`
        to consider just those columns specified
        here as "foreign".

    2. The :class:`_schema.Table` being mapped does not actually have
        :class:`_schema.ForeignKey` or
        :class:`_schema.ForeignKeyConstraint`
        constructs present, often because the table
        was reflected from a database that does not support foreign key
        reflection (MySQL MyISAM).

    3. The :paramref:`_orm.relationship.primaryjoin`
        argument is used to
        construct a non-standard join condition, which makes use of
        columns or expressions that do not normally refer to their
        "parent" column, such as a join condition expressed by a
        complex comparison using a SQL function.

    The :func:`_orm.relationship` construct will raise informative
    error messages that suggest the use of the
    :paramref:`_orm.relationship.foreign_keys` parameter when
    presented with an ambiguous condition.   In typical cases,
    if :func:`_orm.relationship` doesn't raise any exceptions, the
    :paramref:`_orm.relationship.foreign_keys` parameter is usually
    not needed.

    :paramref:`_orm.relationship.foreign_keys` may also be passed as a
    callable function which is evaluated at mapper initialization time,
    and may be passed as a Python-evaluable string when using
    Declarative.

    .. warning:: When passed as a Python-evaluable string, the
        argument is interpreted using Python's ``eval()`` function.
        **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
        See :ref:`declarative_relationship_eval` for details on
        declarative evaluation of :func:`_orm.relationship` arguments.

    .. seealso::

    :ref:`relationship_foreign_keys`

    :ref:`relationship_custom_foreign`

    :func:`.foreign` - allows direct annotation of the "foreign"
    columns within a :paramref:`_orm.relationship.primaryjoin`
    condition.

:param primaryjoin:
    A SQL expression that will be used as the primary
    join of the child object against the parent object, or in a
    many-to-many relationship the join of the parent object to the
    association table. By default, this value is computed based on the
    foreign key relationships of the parent and child tables (or
    association table).

    :paramref:`_orm.relationship.primaryjoin` may also be passed as a
    callable function which is evaluated at mapper initialization time,
    and may be passed as a Python-evaluable string when using
    Declarative.

    .. warning:: When passed as a Python-evaluable string, the
        argument is interpreted using Python's ``eval()`` function.
        **DO NOT PASS UNTRUSTED INPUT TO THIS STRING**.
        See :ref:`declarative_relationship_eval` for details on
        declarative evaluation of :func:`_orm.relationship` arguments.

    .. seealso::

        :ref:`relationship_primaryjoin`
```