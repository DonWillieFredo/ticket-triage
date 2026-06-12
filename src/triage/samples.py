"""Realistic facilities maintenance work-order sample data for development and tests."""

from typing import TypedDict


class WorkOrderSample(TypedDict):
    id: str
    raw_text: str
    reported_by: str
    location: str
    asset: str
    created_at: str
    expected_trade: str
    expected_priority: str
    safety_notes: list[str]


REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "raw_text",
    "reported_by",
    "location",
    "asset",
    "created_at",
    "expected_trade",
    "expected_priority",
    "safety_notes",
)

WORK_ORDERS: list[WorkOrderSample] = [
    {
        "id": "WO-2024-0001",
        "raw_text": (
            "Toilet over flowing on 2nd floor near elevator, water everywhere. "
            "Pretty bad — tenants walking through it."
        ),
        "reported_by": "Maria Santos (Building Manager)",
        "location": "2nd Floor — Elevator Lobby, Suite 210 corridor",
        "asset": "Restroom — Men's, 2nd Floor East",
        "created_at": "2024-03-04T06:42:00-05:00",
        "expected_trade": "plumbing",
        "expected_priority": "urgent",
        "safety_notes": [
            "Slip hazard from standing water; keep area cordoned if possible.",
        ],
    },
    {
        "id": "WO-2024-0002",
        "raw_text": (
            "Strong rotten egg smell in basement mechanical room. Started about 20 min ago. "
            "Not sure if it's the boiler or something else. Getting worse."
        ),
        "reported_by": "Night Security — Desk 1",
        "location": "Basement — Mechanical Room B",
        "asset": "Boiler #2 — Weil-McLain",
        "created_at": "2024-03-04T22:15:00-05:00",
        "expected_trade": "hvac",
        "expected_priority": "emergency",
        "safety_notes": [
            (
                "Possible gas leak — do not operate electrical switches in area; "
                "evacuate adjacent spaces and call gas utility if smell persists."
            ),
        ],
    },
    {
        "id": "WO-2024-0003",
        "raw_text": (
            "Water dripping from ceiling tile in electrical closet. Pooling on floor "
            "and I can see it running down the wall near the panel. Breaker room smells burnt."
        ),
        "reported_by": "Facilities Tech — Jake",
        "location": "1st Floor — Electrical Closet EC-104",
        "asset": "Main Distribution Panel MDP-104",
        "created_at": "2024-03-05T09:18:00-05:00",
        "expected_trade": "electrical",
        "expected_priority": "emergency",
        "safety_notes": [
            (
                "Active water intrusion near energized equipment — lock out panel, "
                "de-energize affected circuits before any contact with water."
            ),
        ],
    },
    {
        "id": "WO-2024-0004",
        "raw_text": (
            "No heat on 5th floor since 6pm. It's 38 outside and the call center "
            "is still staffed until midnight. People are complaining it's freezing."
        ),
        "reported_by": "Call Center Supervisor — Dana",
        "location": "5th Floor — Open Office, West Wing",
        "asset": "AHU-5 West — Rooftop Unit",
        "created_at": "2024-03-05T20:33:00-05:00",
        "expected_trade": "hvac",
        "expected_priority": "urgent",
        "safety_notes": [
            (
                "After-hours HVAC failure in occupied building — monitor for pipe freeze "
                "if outdoor temps drop further."
            ),
        ],
    },
    {
        "id": "WO-2024-0005",
        "raw_text": (
            "3rd floor women's restroom completely clogged. Won't flush, water backing up "
            "into the bowl. Already had one overflow this morning."
        ),
        "reported_by": "Tenant — Apex Legal, Suite 320",
        "location": "3rd Floor — Restroom 3W",
        "asset": "Toilet — Restroom 3W, Stall 2",
        "created_at": "2024-03-06T08:05:00-05:00",
        "expected_trade": "plumbing",
        "expected_priority": "high",
        "safety_notes": [
            "Sanitation and repeat overflow risk — take restroom out of service if backup continues.",
        ],
    },
    {
        "id": "WO-2024-0006",
        "raw_text": (
            "Loading dock exterior door won't latch. You can pull it open even when "
            "the handle shows locked. Delivery drivers propping it open with pallets."
        ),
        "reported_by": "Receiving Clerk — Tom",
        "location": "Loading Dock — Door LD-02",
        "asset": "Exterior Steel Door LD-02 + Panic Hardware",
        "created_at": "2024-03-06T14:22:00-05:00",
        "expected_trade": "general",
        "expected_priority": "high",
        "safety_notes": [
            "Security breach — unsecured exterior door; post temp guard or monitor until repaired.",
        ],
    },
    {
        "id": "WO-2024-0007",
        "raw_text": (
            "Half the parking lot lights are out on the north side. Dark when staff "
            "leave after 7pm. Someone almost tripped on a curb last night."
        ),
        "reported_by": "HR Admin — Priya",
        "location": "North Parking Lot — Rows N1 through N4",
        "asset": "Pole Lights — Fixtures PL-N01 through PL-N06",
        "created_at": "2024-03-07T17:45:00-05:00",
        "expected_trade": "electrical",
        "expected_priority": "medium",
        "safety_notes": [
            "Poor exterior lighting — trip and security risk after dark.",
        ],
    },
    {
        "id": "WO-2024-0008",
        "raw_text": (
            "Carpet tile peeled up in main hallway outside conference room B. "
            "Corner sticking up about 3 inches. Almost caught my cart wheel."
        ),
        "reported_by": "Mailroom — Carlos",
        "location": "2nd Floor — Main Corridor outside Conf Room B",
        "asset": "Carpet Tile — Corridor Section C-2B",
        "created_at": "2024-03-08T11:30:00-05:00",
        "expected_trade": "general",
        "expected_priority": "medium",
        "safety_notes": [
            "Active trip hazard in high-traffic corridor — mark or tape down until repair.",
        ],
    },
    {
        "id": "WO-2024-0009",
        "raw_text": (
            "There's a leak somewhere on the 4th floor. I hear dripping but I can't "
            "find where it's coming from. Maybe above the ceiling?"
        ),
        "reported_by": "Tenant — BrightPath Consulting",
        "location": "",
        "asset": "",
        "created_at": "2024-03-08T15:10:00-05:00",
        "expected_trade": "plumbing",
        "expected_priority": "medium",
        "safety_notes": [],
    },
    {
        "id": "WO-2024-0010",
        "raw_text": (
            "Something is broken in the basement. Making a loud banging noise every "
            "few minutes. I don't know what equipment it is."
        ),
        "reported_by": "Janitorial — Night Crew Lead",
        "location": "Basement — Storage Area",
        "asset": "",
        "created_at": "2024-03-09T01:55:00-05:00",
        "expected_trade": "general",
        "expected_priority": "medium",
        "safety_notes": [],
    },
    {
        "id": "WO-2024-0011",
        "raw_text": (
            "Outlet in breakroom sparking when we plug in the microwave. "
            "Burn mark on the plate. We unplugged everything."
        ),
        "reported_by": "Tenant — DataFlow Inc, Suite 512",
        "location": "5th Floor — Breakroom 5BR",
        "asset": "Duplex Receptacle — Breakroom South Wall",
        "created_at": "2024-03-09T12:08:00-05:00",
        "expected_trade": "electrical",
        "expected_priority": "urgent",
        "safety_notes": [
            "Fire and shock hazard — keep circuit de-energized until inspected.",
        ],
    },
    {
        "id": "WO-2024-0012",
        "raw_text": (
            "Elevator 2 making grinding noise between floors 3 and 4. Passengers "
            "reported a jolt. Still running but sounds wrong."
        ),
        "reported_by": "Front Desk — Reception",
        "location": "Elevator Bank — Car 2",
        "asset": "Passenger Elevator #2 — Otis Gen2",
        "created_at": "2024-03-10T07:20:00-05:00",
        "expected_trade": "general",
        "expected_priority": "urgent",
        "safety_notes": [
            "Potential entrapment risk — vendor callback required; consider pulling from service.",
        ],
    },
    {
        "id": "WO-2024-0013",
        "raw_text": (
            "Weird chemical smell on one of the upper floors. Can't pin down where. "
            "Two people left early because of headaches."
        ),
        "reported_by": "Anonymous tenant call",
        "location": "",
        "asset": "",
        "created_at": "2024-03-10T13:40:00-05:00",
        "expected_trade": "hvac",
        "expected_priority": "high",
        "safety_notes": [
            (
                "Possible IAQ issue — investigate HVAC intake and nearby chemical storage; "
                "consider temporary ventilation boost."
            ),
        ],
    },
    {
        "id": "WO-2024-0014",
        "raw_text": (
            "Roof leak in mechanical room. Water coming through ceiling around "
            "pipe penetrations. Dripping onto insulation and floor drain is slow."
        ),
        "reported_by": "Building Engineer — Ray",
        "location": "Roof Level — Mechanical Penthouse",
        "asset": "Roof Membrane — Section Penthouse North",
        "created_at": "2024-03-11T06:00:00-05:00",
        "expected_trade": "general",
        "expected_priority": "high",
        "safety_notes": [
            "Water near rooftop electrical equipment — verify no active leaks onto live gear.",
        ],
    },
    {
        "id": "WO-2024-0015",
        "raw_text": (
            "Fire alarm panel showing trouble on 2nd floor smoke detector. "
            "Intermittent chirp in hallway near stair 2."
        ),
        "reported_by": "Life Safety Monitor — Central Station Callback",
        "location": "2nd Floor — Stair 2 Corridor",
        "asset": "Smoke Detector — SD-2F-14",
        "created_at": "2024-03-11T09:52:00-05:00",
        "expected_trade": "electrical",
        "expected_priority": "high",
        "safety_notes": [
            "Life safety system impairment — restore detector to normal within 4 hours per policy.",
        ],
    },
    {
        "id": "WO-2024-0016",
        "raw_text": (
            "Ice machine in cafeteria leaking steadily. Puddle spreading toward "
            "the serving line. Already mopped twice this shift."
        ),
        "reported_by": "Cafeteria Manager — Linda",
        "location": "1st Floor — Cafeteria Kitchen",
        "asset": "Ice Machine — Hoshizaki KM-515",
        "created_at": "2024-03-12T10:15:00-05:00",
        "expected_trade": "plumbing",
        "expected_priority": "medium",
        "safety_notes": [
            "Slip hazard near food service area.",
        ],
    },
    {
        "id": "WO-2024-0017",
        "raw_text": (
            "Office window cracked on 6th floor. Looks like something hit it from "
            "outside. Glass still in frame but spiderwebbed."
        ),
        "reported_by": "Tenant — Meridian Finance, Suite 620",
        "location": "6th Floor — Office 620, Window W3",
        "asset": "Exterior Window — Unit 620-W3",
        "created_at": "2024-03-12T14:30:00-05:00",
        "expected_trade": "general",
        "expected_priority": "medium",
        "safety_notes": [
            "Potential falling glass hazard at height — restrict access below if instability worsens.",
        ],
    },
    {
        "id": "WO-2024-0018",
        "raw_text": (
            "Sprinkler head in warehouse aisle 7 dripping constantly. Small puddle "
            "on concrete. Not sure if it's a leak or just a bad head."
        ),
        "reported_by": "Warehouse Supervisor — Mike",
        "location": "Warehouse — Aisle 7, Bay 12",
        "asset": "Sprinkler Head — WH-A7-12",
        "created_at": "2024-03-13T08:45:00-05:00",
        "expected_trade": "plumbing",
        "expected_priority": "high",
        "safety_notes": [
            "Fire suppression system impairment — do not hang items from head; expedite repair.",
        ],
    },
    {
        "id": "WO-2024-0019",
        "raw_text": (
            "Its way too hot in here. AC doesn't seem to be doing anything. "
            "Thermostat says 78 and it's only 9am."
        ),
        "reported_by": "Tenant — Unknown caller, Suite 400 area",
        "location": "4th Floor",
        "asset": "",
        "created_at": "2024-03-13T11:20:00-05:00",
        "expected_trade": "hvac",
        "expected_priority": "medium",
        "safety_notes": [],
    },
    {
        "id": "WO-2024-0020",
        "raw_text": (
            "Stairwell light between 3rd and 4th floor flickering and goes dark "
            "for a few seconds at a time. Hard to see the steps."
        ),
        "reported_by": "Tenant — GreenLeaf Design, Suite 310",
        "location": "Stair 1 — Landing between Floors 3 and 4",
        "asset": "Stairwell Light Fixture — ST1-3L",
        "created_at": "2024-03-14T16:05:00-05:00",
        "expected_trade": "electrical",
        "expected_priority": "medium",
        "safety_notes": [
            "Egress lighting deficiency — prioritize before next occupancy period.",
        ],
    },
]
