using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using NagyprojektBackend.Data;
using System.Linq;

namespace NagyprojektBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class DashboardController : ControllerBase
    {
        private readonly AppDbContext _db;
        public DashboardController(AppDbContext db) => _db = db;

        [HttpGet("summary")]
        public IActionResult Summary()
        {
            var totalUsers = _db.Users.Count();
            var totalGroups = _db.Groups.Count();
            var totalTags = _db.RfidTags.Count();
            var recentLogs = _db.Logs.OrderByDescending(l => l.Timestamp).Take(10).Select(l => new { l.Id, l.Timestamp, l.Message }).ToList();

            return Ok(new { totalUsers, totalGroups, totalTags, recentLogs });
        }
    }
}
