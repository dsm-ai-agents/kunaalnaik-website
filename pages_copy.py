"""Page copy aggregator for the KunaalNaik.com static generator."""

from pages_services import SERVICES
from pages_home import build_home
from pages_about import build_about_group
from pages_gcc import build_gcc_case
from pages_legal import CONTACT_FAQS, build_legal


def make_bodies(*, page_hero, cta, scorecard_cta, sidebar, mailto, faq_section,
                 EMAIL, ENGAGEMENT_FLOOR, SOCIALS):
    """Return homepage and static-page HTML bodies using build.py helpers."""
    home = build_home(mailto=mailto, scorecard_cta=scorecard_cta, cta=cta)
    about, speaking, cases, insights = build_about_group(
        page_hero=page_hero, sidebar=sidebar, cta=cta)
    gcc_case = build_gcc_case(page_hero=page_hero, sidebar=sidebar, cta=cta)
    contact, privacy, terms, not_found = build_legal(
        page_hero=page_hero, mailto=mailto, faq_section=faq_section,
        scorecard_cta=scorecard_cta, EMAIL=EMAIL,
        ENGAGEMENT_FLOOR=ENGAGEMENT_FLOOR, SOCIALS=SOCIALS)
    return {
        "home": home,
        "about": about,
        "speaking": speaking,
        "cases": cases,
        "gcc_case": gcc_case,
        "insights": insights,
        "contact": contact,
        "privacy": privacy,
        "terms": terms,
        "not_found": not_found,
    }
