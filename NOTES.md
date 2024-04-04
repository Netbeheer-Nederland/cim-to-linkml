# Notes

* Tightly couple these models with EA? For example: make the EA object IDs part of them?
* Package author is available in `t_object`
* Add `ea_guid`? Niet mee joinen, want is niet indexed
* Leave out `t_object.alias` for now
* `t_package.Notes` vs `t_object.Note`: which one to choose?
    SELECT o.Note, p.Notes FROM t_object o
    LEFT JOIN t_package p ON o.Object_ID = p.Package_ID
    WHERE o.Object_Type = "Package"
* There are two classes with a parent. What does it mean and should I do something with it?
    select * from t_object where Object_Type = "Class"
    and ParentID != 0
* Every `t_connector.Name` is NULL
* Every `t_connector.Notes` is NULL
* What do certain fields mean in `t_connector`?
    - source/dest role `Containment`? (NULL/Reference/Unspecified)
    - qualifiers?
* The enum of connector types is limited to what it is used, it's not complete (as in `t_objecttypes`)
* We are ignoring the stereotypes of connectors currently
* NOTE: connectors don't have links to packages. I expected them to actually...
* IMPORTANT: packages are not independent. A class in package A can have an attribute with a class as range from package B.
    - This means it makes no sense to generate a schema based on a package and be done with it. You need access to other packages as well
    - Can I make the assumption that a name of a class uniquely identifies it even across packages?! How else will I make this work solidly?
    - Maybe it suffices to inherit the classes from the superpackages of the package?
- Class objects with duplicate names
    {'Profile', 'IEC61968CIMVersion', 'TroubleReportingKind', 'ResourceCertification'}
- "Formally, the Package is a Namespace for the members it contains, and a model element can be a member of one and only one Package. In software engineering and other formal modeling disciplines a Package can be set as a Namespace Root, which acts as the starting point of a given namespace." (https://sparxsystems.com/enterprise_architect_user_guide/16.1/modeling_fundamentals/packagetasks.html)
- Write your own serializer, based on theirs.
    - Underscoring in a better way than LinkML does.
    - Escaping/removing/replacing dangerous characters.
    - Compact notation of annotations
- Tidy up all the gen_safe() and camel_case stuff all over the place. Lots of repetition.