using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using NagyprojektBackend.Data;
using NagyprojektBackend.Models;

namespace NagyprojektBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class GroupsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public GroupsController(AppDbContext db) => _db = db;

        [HttpGet]
        public IActionResult GetAll() => Ok(_db.Groups.ToList());

        [HttpPost]
        public IActionResult Create([FromBody] Group group)
        {
            _db.Groups.Add(group);
            _db.SaveChanges();
            return CreatedAtAction(nameof(Get), new { id = group.Id }, group);
        }

        [HttpGet("{id}")]
        public IActionResult Get(int id)
        {
            var g = _db.Groups.Find(id);
            if (g == null) return NotFound();
            return Ok(g);
        }
    }
}
