---
name: freelance-competitor-analyzer
description: |
  Analyze competing freelances on LinkedIn, Upwork, portfolio sites, and industry directories to provide competitive intelligence for sales strategy and market positioning. Use this skill whenever the user mentions competitor analysis, freelance market research, competitive positioning, sales intelligence, market benchmarking, pricing strategy, capability comparison, or wants to understand their competitive landscape in the freelance/consultant market. This skill gathers structured data about competitors' profiles, pricing models, service offerings, market positioning, client testimonials, and technology stacks to inform strategic positioning and pricing decisions.
compatibility: ""
---

# Freelance Competitor Analyzer

## Purpose

Analyze competing freelances and consultants across major platforms (LinkedIn, Upwork, portfolio sites, industry directories) to provide structured competitive intelligence. This skill helps identify market opportunities, benchmark pricing, understand capability positioning, and inform go-to-market strategies.

## When to Use This Skill

Trigger this skill when the user:
- Wants to understand competitor pricing and service models
- Needs market positioning recommendations
- Is researching competitive capabilities in a specific niche
- Wants to benchmark their own offering against competitors
- Is planning pricing strategy or service packaging
- Needs sales intelligence for a specific market segment
- Is researching market demand and competitive density

## Input Requirements

The skill accepts:
- **Market Segment**: AI consultant, digital marketer, software developer, etc.
- **Geographic Market**: Specific region/country or "Global"
- **Service Category**: Core service type or specific skill set
- **Analysis Depth**: Quick overview vs. comprehensive competitive landscape
- **Output Focus**: Pricing focus, capability focus, positioning focus, or all-inclusive

## Output Format

The skill produces a structured **Competitive Analysis Report** with:

```
# Competitive Analysis Report: [Market Segment]

## Executive Summary
- Market overview: Number of active competitors, market saturation level
- Average pricing range: Entry-level, mid-market, premium tiers
- Top positioning strategies identified
- Key market opportunities and gaps

## Competitor Profiles (5-10 key competitors)
### Competitor [Name/Alias]
- **Platform(s)**: Where they're active (LinkedIn, Upwork, portfolio, etc.)
- **Experience Level**: Years in market, specialization depth
- **Service Offerings**: Core services, differentiators, package types
- **Pricing Model**: Hourly rate / project-based / retainer, typical range
- **Market Position**: Generalist vs. specialist, premium vs. budget
- **Client Base**: Target client type, company sizes, industries
- **Key Differentiators**: Unique value propositions, certifications, achievements
- **Technology Stack**: Tools, platforms, methodologies used
- **Social Proof**: Client testimonials, case studies, ratings/reviews

## Pricing Benchmark Analysis
- **Entry-Level Tier**: Typical rates, service scope, target clients
- **Mid-Market Tier**: Standard market rates, comprehensive service packages
- **Premium Tier**: High-end rates, specialized expertise, niche positioning
- **Pricing Trends**: Are rates rising, stabilizing, or declining?

## Capability Mapping Matrix
[Table showing competitors mapped across key capabilities like: Technical depth, Industry specialization, Communication skills, Project management, Certifications, etc.]

## Market Positioning Analysis
- **Premium Positioning**: Competitors competing on quality/expertise
- **Value Positioning**: Competitors competing on affordability/efficiency
- **Niche Positioning**: Competitors competing on specialization
- **Brand Positioning**: Competitors competing on reputation/network

## Market Opportunities & Gaps
- **Underserved niches**: Market segments with few competitors
- **Pricing gaps**: Price points without strong competitor presence
- **Capability gaps**: Service types with limited competitor offerings
- **Geographic gaps**: Regions with limited specialized competition

## Strategic Recommendations
- Recommended positioning strategy based on competitive landscape
- Pricing recommendations relative to competitive average
- Differentiation suggestions based on identified gaps
- Target market segments with lowest competitive density
- Capability development priorities

## Market Saturation Assessment
- Competition density: Low / Moderate / High
- Market trend: Growing / Stable / Declining
- Entry difficulty: Easy / Moderate / Difficult
```

## Execution Steps

1. **Identify Target Market**: Clarify the market segment and geographic focus
2. **Research Platforms**: Search LinkedIn, Upwork, portfolio aggregators, industry directories
3. **Competitor Discovery**: Identify 5-10 relevant competitors based on filters:
   - Similar service offerings
   - Overlapping target market
   - Comparable experience level or aspiration
4. **Profile Analysis**: For each competitor, extract:
   - Pricing information (from profile, previous projects, rate cards)
   - Service scope and offerings
   - Client testimonials and social proof
   - Experience and certifications
   - Technology stack and methodologies
   - Market positioning signals
5. **Data Synthesis**: Aggregate findings into benchmark analysis and positioning insights
6. **Recommendations**: Synthesize strategic recommendations based on competitive landscape

## Data Sources

- **LinkedIn**: Freelancer profiles, service offerings, endorsements, recommendations
- **Upwork**: Pricing, portfolio projects, client feedback, rates, specializations
- **Portfolio Sites**: Personal websites, portfolio.com, behance.net, dribbble.com
- **Industry Directories**: Specialized directories for consultants, agencies, experts
- **Public Reviews**: Google Reviews, Trustpilot, industry-specific review sites
- **Published Content**: Blog posts, case studies, whitepapers indicating expertise

## Assumptions & Limitations

- Analysis based on publicly available information only
- Pricing estimates inferred from public rates; actual pricing may vary
- Analysis represents point-in-time snapshot; market may have changed
- Only analyzes visible online presence; some competitors may be less public
- Geographic pricing variations not fully captured in global market view
- Assumes English-language sources unless specified otherwise

## Example Usage

**User Input:**
"Analyze competitors in the AI consulting space. I'm targeting enterprise clients in the US market. Focus on pricing and positioning strategy."

**Skill Output:**
Comprehensive competitive analysis report with 8-10 key competitors profiled, pricing benchmarks across 3 tiers, capability mapping matrix, market positioning analysis, identified opportunities/gaps, and strategic recommendations for pricing and differentiation.
