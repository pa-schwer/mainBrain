import { describe, expect, it } from "vitest";
import { absoluteUrl } from "../src/lib/url";

describe("absoluteUrl", () => {
  it("joins the site and a path whatever the slashes", () => {
    expect(absoluteUrl("https://{{DOMAIN}}", "/privacy")).toBe("https://{{DOMAIN}}/privacy");
    expect(absoluteUrl("https://{{DOMAIN}}/", "privacy")).toBe("https://{{DOMAIN}}/privacy");
    expect(absoluteUrl("https://{{DOMAIN}}", "/")).toBe("https://{{DOMAIN}}/");
  });
});
