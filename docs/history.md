# HamStack: background and history

HamStack grew out of Ham Radio Village conference work: a recurring need to
stand up useful amateur-radio computing infrastructure quickly, cheaply, and
repeatably without turning every event into an exercise in reconstructing a
one-off Raspberry Pi from shell history.

The early concept was deliberately small: a few Raspberry Pi 4 systems that
could be repurposed into useful radio nodes for a conference. Those experiments
included packet radio, an RF bulletin-board system, SSTV, AllStar, digital-mode
software, SDR receive services, and 44Net connectivity. The same hardware-hacker
mindset that produced projects such as **Can It Ham?** also shaped HamStack:
use ordinary hardware, make the radio side visible and interactive, tolerate
failure, and make it easy to rebuild the thing when somebody inevitably changes
the plan at 02:00 before an event.

DEF CON 34 became an important proving ground. Two examples from that work now
inform HamStack directly:

- the multi-band packet node/BBS design, where Graywolf provided modem/PTT
  services and LinBPQ consumed one loopback KISS TCP endpoint per radio channel;
- the headless SSTV Selfie Station, built around a Raspberry Pi, Pi Camera, USB
  foot pedal, PySSTV, and an AIOC for audio/PTT.

The reference deployment continued to evolve beyond the original three-node
concept. Additional Raspberry Pi and Pi Zero systems took on specialized jobs
such as WPSD, AllStar, SSTV, packet/BBS work, and the Selfie Station. That
evolution exposed the real problem HamStack needed to solve: the useful unit was
not a prebuilt SD-card image or one person's exact collection of Pis. The useful
unit was a **repeatable configuration model**.

That is the project today.

HamStack is an open-source Ansible framework for turning already bootable,
reachable Linux or appliance-style systems into radio-computing nodes. The
operator installs a supported base OS or upstream image, primes the machine for
Ansible, describes the desired hardware and roles in inventory, and lets
HamStack apply the configuration.

The local Ham Radio Village deployment is the project's reference environment,
not the definition of the project. Other neighborhoods and operators should be
able to use different computers, radios, interfaces, network layouts, and role
combinations without forking the architecture.

## Design principles

HamStack tries to remain:

- **Reproducible** — a node should be reconstructable from a known starting
  state plus inventory.
- **Hardware-flexible** — roles describe capabilities rather than requiring one
  exact Raspberry Pi model.
- **Composable** — one host may run several roles and several roles may share a
  named hardware resource such as an AIOC.
- **Upstream-friendly** — appliance projects such as WPSD and AllStarLink remain
  upstream projects; HamStack configures them rather than pretending to replace
  their installers.
- **Conference-tolerant** — services should have sane offline behavior, avoid
  unnecessary plaintext management traffic, and fail clearly when a dependency
  is missing.
- **Incremental** — a simple, validated role is preferred to an elaborate role
  that merely looks finished.
- **Operator-controlled** — transmitting behavior, credentials, routing, and
  other consequential settings are explicit variables rather than hidden magic.

## What HamStack is not

HamStack is not a monolithic appliance image, a Kubernetes distribution, or an
attempt to hide amateur radio behind an opaque dashboard. It is also not a
promise that every listed role is appropriate for every computer.

The project documents a reference hardware set and expected capability classes,
but a deployment remains responsible for matching workload to hardware and for
operating radio equipment lawfully.
