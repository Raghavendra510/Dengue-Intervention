(define (problem dengue-hotspot-d02)
  (:domain dengue-intervention)
  
  (:objects
    team1 - team
    d01 d02 - location
  )

  (:init
    (at team1 d01)
    (adjacent d01 d02)
    (adjacent d02 d01)
    (uninspected d02)
  )

  (:goal
    (and
      (safe d02)
    )
  )
)

