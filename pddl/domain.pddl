(define (domain dengue-intervention)
  (:requirements :strips :typing)
  (:types location team)
  
  (:predicates
    (at ?t - team ?l - location)
    (adjacent ?l1 - location ?l2 - location)
    (uninspected ?l - location)
    (inspected ?l - location)
    (breeding_site_confirmed ?l - location)
    (sprayed ?l - location)
    (cases_treated ?l - location)
    (safe ?l - location)
  )

  (:action move
    :parameters (?t - team ?from - location ?to - location)
    :precondition (and (at ?t ?from) (adjacent ?from ?to))
    :effect (and (not (at ?t ?from)) (at ?t ?to))
  )

  (:action inspect_zone
    :parameters (?t - team ?l - location)
    :precondition (and (at ?t ?l) (uninspected ?l))
    :effect (and (not (uninspected ?l)) (inspected ?l) (breeding_site_confirmed ?l))
  )

  (:action spray_larvicide
    :parameters (?t - team ?l - location)
    :precondition (and (at ?t ?l) (breeding_site_confirmed ?l))
    :effect (and (sprayed ?l))
  )

  (:action treat_patients
    :parameters (?t - team ?l - location)
    :precondition (and (at ?t ?l) (sprayed ?l))
    :effect (and (cases_treated ?l))
  )

  (:action certify_safe
    :parameters (?l - location)
    :precondition (and (sprayed ?l) (cases_treated ?l))
    :effect (and (safe ?l))
  )
)

